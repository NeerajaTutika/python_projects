from cryptography.fernet import Fernet
import json
import os

class Notes:

    def __init__(self, notes_file="data.json", key_file="secret.key"):
        self.notes_file = notes_file
        self.key_file = key_file
        self.notes = []
        self.fernet = None
        self.set_fernet()
        self.load_notes()

    def set_fernet(self):
        
        if os.path.exists(self.key_file):
            with open(self.key_file, "rb") as f:
                crypto_key = f.read()
            print("Encryption key loaded successfully!")
        else:
            crypto_key = Fernet.generate_key()
            with open(self.key_file, "wb") as f:
                f.write(crypto_key)
            print("Encryption key created and saved.")
        self.fernet = Fernet(crypto_key)

    def encrypt_text(self, text):
        """Encrypt the given text using the fernet key."""
        if not self.fernet:
            raise ValueError("Fernet key is not set.")
        return self.fernet.encrypt(text.encode()).decode()
    
    def decrypt_text(self, encrypted_text):
        """Decrypt the given encrypted text using the fernet key."""
        if not self.fernet:
            raise ValueError("Fernet key is not set.")
        return self.fernet.decrypt(encrypted_text.encode()).decode()
    
    def save_notes(self):
        try:
            with open(self.notes_file, 'w') as file:
                json.dump(self.notes, file, indent=4)
        except Exception as e:
            print(f"Error saving notes: {e}")
    
    def load_notes(self):
        try:
            with open(self.notes_file, 'r') as file:
                self.notes = json.load(file)
        except FileNotFoundError:
            self.notes = []
        except json.JSONDecodeError:
            self.notes = []
            print("Warning: Error decoding JSON from notes file. Starting with an empty notes list.")
        except Exception as e:
            self.notes = []
            print(f"Error loading notes: {e}")
    
    def add_note(self):
        print("Add a new note...")
        title = input("Enter note title: ").strip()
        if not title:
            print("Title cannot be empty.")
            return
        content = input("Enter note content: ").strip()
        if not content:
            print("Content cannot be empty.")
            return
        
        try:
            encrypted_content = self.encrypt_text(content)
            note_id = self.get_next_id()
            note = {
                "id": note_id,
                "title": title,
                "content": encrypted_content
            }
            self.notes.append(note)
            self.save_notes()
            print("Note added successfully!")
        except Exception as e:
            print(f"Error adding note: {e}")

    def get_next_id(self):
        """Get the next available note ID."""
        if not self.notes:
            return 1
        return max(note['id'] for note in self.notes) + 1

    def list_notes(self):
        if not self.notes:
            print("No notes available.")
            return

        print("\nYour Notes:")
        for note in self.notes:
            preview = ""
            try:
                preview = self.decrypt_text(note['content'])[:20] + "..."
            except Exception:
                preview = "[Cannot decrypt preview]"
            print(f"ID: {note['id']}, Title: {note['title']}, Preview: {preview}")

    def get_note_by_id(self, note_id):
        """Retrieve a note by its ID."""
        for note in self.notes:
            if note['id'] == note_id:
                return note
        return None

    def view_note(self):
        if not self.notes:
            print("No notes available.")
            return
        self.list_notes()
        try:
            note_id = int(input("Enter the ID of the note you want to view: ").strip())
            note = self.get_note_by_id(note_id)

            if note is None:
                print("Note not found.")
                return
            
            try:
                decrypted_text = self.decrypt_text(note['content'])
            except Exception:
                print("Error decrypting note content. The note may have been encrypted with a different key.")
                return

            print(f"\nNote ID: {note['id']}")
            print(f"Title: {note['title']}")
            print(f"Content: {decrypted_text}")
        except ValueError:
            print("Invalid input. Please enter a valid note ID.")
        except Exception as e:
            print(f"Error viewing note: {e}")

    def delete_note(self):
        if not self.notes:
            print("No notes available.")
            return
        self.list_notes()
        try:
            note_id = int(input("Enter the ID of the note you want to delete: ").strip())
            note = self.get_note_by_id(note_id)

            if note is None:
                print("Note not found.")
                return
            
            for i, n in enumerate(self.notes):
                if n['id'] == note_id:
                    deleted_note = self.notes.pop(i)
                    self.save_notes()
                    print(f"Deleted note: {deleted_note['title']}")
                    return
        except ValueError:
            print("Invalid input. Please enter a valid note ID.")
        except Exception as e:
            print(f"Error deleting note: {e}")

    def export_notes(self):
        """Export all decrypted notes to a text file for backup."""
        export_file = input("Enter filename to export notes (e.g., backup.txt): ").strip()
        if not export_file:
            print("Export cancelled.")
            return
        try:
            with open(export_file, "w", encoding="utf-8") as f:
                for note in self.notes:
                    try:
                        content = self.decrypt_text(note['content'])
                    except Exception:
                        content = "[Cannot decrypt note]"
                    f.write(f"ID: {note['id']}\nTitle: {note['title']}\nContent: {content}\n\n")
            print(f"Notes exported to {export_file}")
        except Exception as e:
            print(f"Error exporting notes: {e}")

    def menu(self):
        print("Notes CLI App")
        while True:
            print("\nOptions:")
            print("1. Add Note")
            print("2. List Notes")
            print("3. View Note")
            print("4. Delete Note")
            print("5. Export Notes")
            print("6. Exit")

            choice = input("Choose an option: ").strip()
            if choice == '1':
                self.add_note()
            elif choice == '2':
                self.list_notes()
            elif choice == '3':
                self.view_note()
            elif choice == '4':
                self.delete_note()
            elif choice == '5':
                self.export_notes()
            elif choice == '6':
                print("Exiting the app.")
                break
            else:
                print("Invalid choice. Please try again.")
        
def main():
    notes = Notes()
    notes.menu()

if __name__ == "__main__":
    main()