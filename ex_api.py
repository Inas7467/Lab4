import requests

class BookSearchApp:
    def __init__(self):
        self.api_url = "https://openlibrary.org/search.json"
        self.books = []  # List to store fetched books

    def get_user_input(self):
        """Get search term from user"""
        return input("Enter a search term (e.g., title, author, or keyword): ")

    def fetch_books(self, query):
        """Send an API request to Open Library to fetch books based on the user's query"""
        try:
            response = requests.get(self.api_url, params={'q': query})
            response.raise_for_status()  # Check if the request was successful
            return response.json()  # Parse and return the JSON data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from the API: {e}")
            return None

    def parse_json_response(self, data):
        """Parse the JSON response to extract relevant book details"""
        if data and "docs" in data and data["numFound"] > 0:
            self.books = []  # Clear previous search results
            for book in data["docs"]:
                title = book.get("title", "No title available")
                authors = book.get("author_name", ["Unknown author"])
                year = book.get("first_publish_year", "Unknown year")
                isbn = book.get("isbn", ["No ISBN available"])[0]  # Get the first ISBN
                self.books.append({
                    "title": title,
                    "author": ', '.join(authors),
                    "year": year,
                    "isbn": isbn
                })
            return self.books
        else:
            return None

    def display_book_details(self, books):
        """Display the details of the books found"""
        if books:
            print(f"\nFound {len(books)} books:\n")
            for idx, book in enumerate(books, start=1):
                print(f"{idx}. {book['title']} by {book['author']} (Published: {book['year']})")
            return True
        else:
            self.handle_no_results()
            return False

    def handle_no_results(self):
        """Handle case when no results are found"""
        print("\nNo results found for the search term. Please try again with a different query.")

    def show_error_message(self, message):
        """Display an error message to the user"""
        print(f"\nError: {message}")

    def view_book_details(self, book):
        """Display detailed information about the selected book"""
        print(f"\nTitle: {book['title']}")
        print(f"Author(s): {book['author']}")
        print(f"Published Year: {book['year']}")
        print(f"ISBN: {book['isbn']}")
        # Here you can add more details if available from the API

    def run(self):
        """Main method to run the book search app"""
        user_query = self.get_user_input()
        if user_query:
            print("\nSearching for books...\n")
            api_response = self.fetch_books(user_query)
            if api_response:
                books = self.parse_json_response(api_response)
                if self.display_book_details(books):
                    self.select_book(books)
            else:
                self.show_error_message("Failed to retrieve data. Please check your network or try again later.")
        else:
            self.show_error_message("Search term cannot be empty.")

    def select_book(self, books):
        """Allow the user to select a book to view details"""
        try:
            choice = int(input("\nEnter the number of the book you want to view details for (0 to exit): "))
            if choice > 0 and choice <= len(books):
                selected_book = books[choice - 1]  # Get the selected book based on index
                self.view_book_details(selected_book)
            elif choice == 0:
                print("Exiting.")
            else:
                print("Invalid choice. Please enter a number corresponding to a book.")
                self.select_book(books)  # Recursion to allow re-selection
        except ValueError:
            print("Please enter a valid number.")
            self.select_book(books)  # Recursion to allow re-selection

# Main program execution
if __name__ == "__main__":
    app = BookSearchApp()
    app.run()
