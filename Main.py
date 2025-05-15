import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime
import os
import csv
import re # For punctuation removal
from collections import Counter # For word counting

# --- Configuration for Dummy CSV ---
DUMMY_CSV_FILENAME = "dummy_reviews.csv"
DUMMY_HEADER = ['review_id', 'reviewer_name', 'review_date', 'rating', 'review_text', 'source']
DUMMY_DATA = [
    ['1', 'John Doe', '2025-04-28', '5', 'Great coffee and atmosphere! Loved it. The staff was friendly.', 'Google_Simulated'],
    ['2', 'Jane Smith', '2025-04-25', '4', 'Good food, service was a bit slow but the food was tasty.', 'Google_Simulated'],
    ['3', 'Alice Brown', '2025-04-22', '5', 'Best cafe in town! Highly recommend the delicious cakes.', 'TripAdvisor_Simulated'],
    ['4', 'Bob Green', '2025-04-18', '2', 'My order was wrong, and it was cold. Terrible coffee too.', 'Google_Simulated'],
    ['5', 'Charlie Blue', '2025-04-15', '4', 'Nice place for a quick bite. Good value.', 'Google_Simulated'],
    ['6', 'Diana Prince', '2025-04-10', '5', 'Excellent service and delicious pastries. Friendly staff always smiling.', 'TripAdvisor_Simulated'],
    ['7', 'Edward Nigma', '2025-04-05', '3', 'It was okay, nothing special. The coffee was average.', 'Google_Simulated'],
    ['8', 'Fiona Glenanne', '2025-04-02', '5', 'Absolutely fantastic! Will be back. Loved the fresh food.', 'Google_Simulated'],
    ['9', 'George Costanza', '2025-03-20', '1', 'Terrible experience. Avoid. Slow service and cold food.', 'Google_Simulated'],
    ['10', 'Helen Troy', '2025-03-15', '4', 'Lovely ambiance, good for meetings. The pastries were fresh.', 'TripAdvisor_Simulated'],
    ['11', 'Ian Malcolm', '2025-05-01', '5', 'Life finds a way... to make great coffee here! Amazing staff.', 'Google_Simulated'],
    ['12', 'Julia Child', '2025-05-03', '4', 'The croissants were delightful, a bit more butter perhaps! Good service.', 'TripAdvisor_Simulated'],
    ['13', 'Kevin McCallister', '2025-02-10', '3', 'Decent, but I\'ve had better pizza. Service was okay.', 'Google_Simulated'],
    ['14', 'Laura Palmer', '2025-04-29', '5', 'The cherry pie is to die for! And the coffee is great.', 'TripAdvisor_Simulated'],
    ['15', 'Michael Scott', '2025-04-12', '4', "That's what she said... about the pretzels! They were good.", 'Google_Simulated'],
    ['16', 'Nancy Drew', '2025-04-08', '5', "Solved the mystery of the missing flavor - it's all here! Excellent food.", 'Google_Simulated'],
    ['17', 'Oscar Wilde', '2025-03-05', '2', 'The coffee is not as good as my wit. And the food was bland.', 'TripAdvisor_Simulated'],
    ['18', 'Peter Pan', '2025-04-20', '5', "Never want to grow up if it means leaving this cafe! Fantastic atmosphere.", 'Google_Simulated'],
    ['19', 'Quinn Fabray', '2025-04-01', '4', 'Good vibes, a bit pricey though. The cakes are worth it.', 'TripAdvisor_Simulated'],
    ['20', 'Rachel Green', '2025-04-16', '3', 'Not bad, but they were out of my favorite muffin. Staff seemed busy.', 'Google_Simulated']
]

# --- General Configuration ---
OUTPUT_CSV_FILENAME_TEMPLATE = "Last_Month_Reviews_{month}_{year}.csv"
EXPECTED_COLUMNS = DUMMY_HEADER

# Basic list of English stop words
STOP_WORDS = set([
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", "into", "is", "it",
    "no", "not", "of", "on", "or", "such", "that", "the", "their", "then", "there", "these",
    "they", "this", "to", "was", "will", "with", "i", "me", "my", "myself", "we", "our", "ours",
    "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself",
    "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs",
    "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is",
    "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does",
    "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while",
    "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during",
    "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off",
    "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why",
    "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "no",
    "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will",
    "just", "don", "should", "now", "ve", "ll", "m", "o", "re", "ain", "d"
])


def create_dummy_csv_if_not_exists():
    """Creates the dummy_reviews.csv file if it doesn't already exist."""
    if not os.path.exists(DUMMY_CSV_FILENAME):
        try:
            with open(DUMMY_CSV_FILENAME, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(DUMMY_HEADER)
                writer.writerows(DUMMY_DATA)
            return f"'{DUMMY_CSV_FILENAME}' created successfully for simulation."
        except Exception as e:
            return f"Error creating '{DUMMY_CSV_FILENAME}': {e}"
    return f"'{DUMMY_CSV_FILENAME}' already exists. Ready for selection."

def preprocess_text(text):
    """Lowercase, remove punctuation, and tokenize text."""
    if not isinstance(text, str): # Handle potential non-string data
        return []
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text) # Remove punctuation
    words = text.split()
    return [word for word in words if word not in STOP_WORDS and word.isalpha() and len(word) > 2] # Keep actual words > 2 chars

class ReviewAnalyzerApp:
    def __init__(self, root_window):
        self.root = root_window
        self.root.title("Guest Review Dashboard - ABC Cafe")
        self.root.geometry("800x850") # Increased height for themes

        self.input_file_path = None
        self.df_reviews = None

        dummy_csv_status = create_dummy_csv_if_not_exists()

        # Main frame to allow scrolling if content overflows
        main_scroll_frame = ttk.Frame(self.root)
        main_scroll_frame.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(main_scroll_frame)
        scrollbar = ttk.Scrollbar(main_scroll_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # --- UI Elements within scrollable_frame ---
        current_row = 0
        file_frame = ttk.LabelFrame(scrollable_frame, text="1. Load Review Data", padding=(10, 5))
        file_frame.grid(row=current_row, column=0, padx=10, pady=10, sticky="ew")
        current_row += 1

        self.select_file_button = ttk.Button(file_frame, text="Select Review CSV File", command=self.select_review_file)
        self.select_file_button.pack(side=tk.LEFT, padx=5)
        self.selected_file_label = ttk.Label(file_frame, text="No file selected")
        self.selected_file_label.pack(side=tk.LEFT, padx=5)

        process_frame = ttk.LabelFrame(scrollable_frame, text="2. Process and Analyze", padding=(10, 5))
        process_frame.grid(row=current_row, column=0, padx=10, pady=5, sticky="ew")
        current_row += 1

        self.analyze_button = ttk.Button(process_frame, text="Fetch & Analyze Last Month's Reviews", command=self.process_reviews, state=tk.DISABLED)
        self.analyze_button.pack(pady=5)
        self.status_label = ttk.Label(process_frame, text="Status: Waiting for file...")
        self.status_label.pack(pady=5)

        self.graph_frame = ttk.LabelFrame(scrollable_frame, text="3. Review Ratings Distribution (Last Month)", padding=(10, 5))
        self.graph_frame.grid(row=current_row, column=0, padx=10, pady=10, sticky="ew")
        # Set a minimum height for the graph frame to ensure it's visible
        self.graph_frame.configure(height=350) 
        self.graph_frame.grid_propagate(False) # Prevent children from shrinking it
        current_row += 1
        self.canvas_widget = None

        # --- Themes Section ---
        self.themes_frame = ttk.LabelFrame(scrollable_frame, text="4. Common Review Themes (Last Month)", padding=(10, 5))
        self.themes_frame.grid(row=current_row, column=0, padx=10, pady=10, sticky="ew")
        current_row += 1
        
        self.positive_themes_label = ttk.Label(self.themes_frame, text="Positive Themes (4-5 stars): Not analyzed yet.")
        self.positive_themes_label.pack(anchor="w", pady=2)
        self.negative_themes_label = ttk.Label(self.themes_frame, text="Negative Themes (1-2 stars): Not analyzed yet.")
        self.negative_themes_label.pack(anchor="w", pady=2)

        # Configure column 0 of scrollable_frame to expand
        scrollable_frame.grid_columnconfigure(0, weight=1)


        self.status_label.config(text=f"Status: {dummy_csv_status} Please select a review CSV file.")
        initial_message = (
            "Welcome to the Review Analyzer!\n\n"
            f"This application simulates API data using '{DUMMY_CSV_FILENAME}'.\n"
            f"{dummy_csv_status}\n\n"
            "1. Click 'Select Review CSV File' to load review data.\n"
            f"   (You can select the auto-generated '{DUMMY_CSV_FILENAME}' or your own similarly formatted CSV.)\n"
            "2. Click 'Fetch & Analyze' to process last month's reviews.\n"
        )
        messagebox.showinfo("Instructions", initial_message)

    def select_review_file(self):
        initial_dir = os.path.dirname(os.path.abspath(__file__)) if '__file__' in locals() else os.getcwd()
        file_path = filedialog.askopenfilename(
            title="Select Review CSV File",
            initialdir=initial_dir,
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )
        if file_path:
            self.input_file_path = file_path
            self.selected_file_label.config(text=os.path.basename(file_path))
            self.status_label.config(text=f"Status: File '{os.path.basename(file_path)}' loaded. Ready to analyze.")
            self.analyze_button.config(state=tk.NORMAL)
            if self.canvas_widget:
                self.canvas_widget.get_tk_widget().destroy()
                self.canvas_widget = None
            self.positive_themes_label.config(text="Positive Themes (4-5 stars): Not analyzed yet.")
            self.negative_themes_label.config(text="Negative Themes (1-2 stars): Not analyzed yet.")
        else:
            self.selected_file_label.config(text="No file selected")
            self.status_label.config(text="Status: File selection cancelled.")
            self.analyze_button.config(state=tk.DISABLED)

    def get_last_month_dates(self):
        today = datetime.date.today()
        first_day_current_month = today.replace(day=1)
        last_day_last_month = first_day_current_month - datetime.timedelta(days=1)
        first_day_last_month = last_day_last_month.replace(day=1)
        return first_day_last_month, last_day_last_month

    def process_reviews(self):
        if not self.input_file_path:
            messagebox.showerror("Error", "Please select a review CSV file first.")
            return

        self.status_label.config(text="Status: Processing reviews...")
        self.root.update_idletasks() 

        try:
            self.df_reviews = pd.read_csv(
                self.input_file_path,
                delimiter=',',
                quotechar='"',
                on_bad_lines='warn',
            )

            if self.df_reviews.empty and os.path.getsize(self.input_file_path) > 50: # Basic check
                messagebox.showerror("Error", "Pandas read the CSV, but it resulted in an empty dataset...")
                self.status_label.config(text="Status: Error - CSV parsing yielded no data.")
                return

            if not all(col in self.df_reviews.columns for col in EXPECTED_COLUMNS):
                missing = [col for col in EXPECTED_COLUMNS if col not in self.df_reviews.columns]
                messagebox.showerror("Error", f"CSV file is missing required columns: {', '.join(missing)}")
                self.status_label.config(text="Status: Error - CSV missing columns.")
                return

            self.df_reviews['review_date'] = pd.to_datetime(self.df_reviews['review_date'], errors='coerce')
            self.df_reviews.dropna(subset=['review_date'], inplace=True)
            # Ensure 'rating' is numeric before filtering
            self.df_reviews['rating'] = pd.to_numeric(self.df_reviews['rating'], errors='coerce')
            self.df_reviews.dropna(subset=['rating'], inplace=True)
            self.df_reviews['rating'] = self.df_reviews['rating'].astype(int)


            start_last_month, end_last_month = self.get_last_month_dates()
            
            df_last_month = self.df_reviews[
                (self.df_reviews['review_date'].dt.date >= start_last_month) &
                (self.df_reviews['review_date'].dt.date <= end_last_month)
            ].copy()

            if df_last_month.empty:
                messagebox.showinfo("No Data", f"No reviews found for last month ({start_last_month.strftime('%B %Y')}).")
                self.status_label.config(text=f"Status: No reviews for {start_last_month.strftime('%B %Y')}.")
                if self.canvas_widget:
                    self.canvas_widget.get_tk_widget().destroy()
                    self.canvas_widget = None
                self.positive_themes_label.config(text="Positive Themes (4-5 stars): No reviews found.")
                self.negative_themes_label.config(text="Negative Themes (1-2 stars): No reviews found.")
                return

            output_csv_name = OUTPUT_CSV_FILENAME_TEMPLATE.format(
                month=start_last_month.strftime("%B"),
                year=start_last_month.year
            )
            # 'rating' was already converted to int before filtering
            df_last_month.to_csv(output_csv_name, index=False, encoding='utf-8')
            self.status_label.config(text=f"Status: Report '{output_csv_name}' generated. Analyzing themes...")

            self.generate_ratings_graph(df_last_month)
            self.analyze_and_display_themes(df_last_month) # New function call

            messagebox.showinfo("Success", f"Analysis complete! Report saved as '{output_csv_name}'.")
            self.status_label.config(text=f"Status: Analysis complete. Report: '{output_csv_name}'.")


        except pd.errors.ParserError as pe:
            error_detail = str(pe)
            match = re.search(r"line (\d+)", error_detail) # re is already imported
            line_info = f" around line {match.group(1)}" if match else ""
            messagebox.showerror("CSV Parsing Error", f"Pandas could not parse the CSV file{line_info}.\nError: {error_detail}...")
            self.status_label.config(text=f"Status: Error - CSV parsing failed{line_info}.")
        except FileNotFoundError:
            messagebox.showerror("Error", f"File not found: {self.input_file_path}")
            self.status_label.config(text="Status: Error - File not found.")
        except pd.errors.EmptyDataError:
            messagebox.showerror("Error", "The selected CSV file is empty.")
            self.status_label.config(text="Status: Error - CSV file is empty.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            self.status_label.config(text=f"Status: Error - {e}")

    def generate_ratings_graph(self, df_to_graph):
        if self.canvas_widget:
            self.canvas_widget.get_tk_widget().destroy()

        # 'rating' column should already be numeric and int from process_reviews
        ratings_counts = df_to_graph['rating'].value_counts().sort_index()
        ratings_counts = ratings_counts.reindex(range(1, 6), fill_value=0)

        fig, ax = plt.subplots(figsize=(7, 4)) # Adjusted figsize for potentially less height
        ratings_counts.plot(kind='bar', ax=ax, color=['#FF6347','#FFA07A','#FFD700','#90EE90','#32CD32'])
        
        ax.set_title(f"Review Ratings ({df_to_graph['review_date'].dt.date.min().strftime('%B %Y')})", fontsize=11)
        ax.set_xlabel("Star Rating", fontsize=9)
        ax.set_ylabel("Number of Reviews", fontsize=9)
        ax.set_xticklabels(ratings_counts.index, rotation=0)
        ax.grid(axis='y', linestyle='--', alpha=0.7)

        for i, count in enumerate(ratings_counts):
            ax.text(i, count + 0.05 * ratings_counts.max(), str(count), ha='center', va='bottom', fontsize=8)

        plt.tight_layout()

        self.canvas_widget = FigureCanvasTkAgg(fig, master=self.graph_frame)
        self.canvas_widget.draw()
        # Use grid for the canvas widget within graph_frame to control its expansion
        self.canvas_widget.get_tk_widget().grid(row=0, column=0, sticky="nsew")
        self.graph_frame.grid_rowconfigure(0, weight=1)    # Allow canvas row to expand
        self.graph_frame.grid_columnconfigure(0, weight=1) # Allow canvas col to expand


    def analyze_and_display_themes(self, df_reviews_month):
        """Analyzes review text for common themes and updates UI labels."""
        positive_reviews_text = " ".join(df_reviews_month[df_reviews_month['rating'] >= 4]['review_text'].astype(str))
        negative_reviews_text = " ".join(df_reviews_month[df_reviews_month['rating'] <= 2]['review_text'].astype(str))

        positive_words = preprocess_text(positive_reviews_text)
        negative_words = preprocess_text(negative_reviews_text)

        positive_counts = Counter(positive_words)
        negative_counts = Counter(negative_words)

        top_n = 7 # Number of top themes to show

        if positive_counts:
            common_positive = ", ".join([word for word, count in positive_counts.most_common(top_n)])
            self.positive_themes_label.config(text=f"Positive Themes (4-5 stars): {common_positive}")
        else:
            self.positive_themes_label.config(text="Positive Themes (4-5 stars): No significant themes found or no positive reviews.")

        if negative_counts:
            common_negative = ", ".join([word for word, count in negative_counts.most_common(top_n)])
            self.negative_themes_label.config(text=f"Negative Themes (1-2 stars): {common_negative}")
        else:
            self.negative_themes_label.config(text="Negative Themes (1-2 stars): No significant themes found or no negative reviews.")
        
        self.status_label.config(text=self.status_label.cget("text").replace("Analyzing themes...", "Themes analyzed."))


if __name__ == "__main__":
    main_window = tk.Tk()
    create_dummy_csv_if_not_exists() 
    app = ReviewAnalyzerApp(main_window)
    main_window.mainloop()

