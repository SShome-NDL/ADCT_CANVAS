import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QPushButton, QVBoxLayout, QAction, \
    QFileDialog, QLabel, QLineEdit, QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import numpy as np
import pandas as pd
import csv
from timeit import default_timer as timer

# Import your custom window
from INTERNAL_SCENE.calc_window import ADCTWindow


# Worker thread to handle the clustering in the background
class ClusteringWorker(QThread):
    progress = pyqtSignal(str)

    def __init__(self, input_file, output_file, threshold):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.threshold = threshold

    def run(self):
        try:
            start = timer()
            self.progress.emit("Clustering started.")

            # LCS from the start
            def lcs_starting_from_first(str1, str2):
                print(f"lcss between '{str1}' and '{str2}'")
                lcs_length = 0
                for c1, c2 in zip(str1, str2):
                    if c1 == c2:
                        lcs_length += 1
                    else:
                        break
                return lcs_lengthfs

            # Read data from the input CSV file
            try:
                data = pd.read_csv(self.input_file)
                data = data['dc.title']
            except Exception as e:
                self.progress.emit(f"Error reading input file: {e}")
                return

            # Create the similarity matrix
            n = len(data)
            similarity_matrix = np.zeros((n, n))

            for i in range(n):
                for j in range(n):
                    if i < j:
                        lcs_value = lcs_starting_from_first(data[i], data[j])
                        min_len = max(len(data[i]), len(data[j]))
                        similarity_matrix[i, j] = (lcs_value / min_len * 100) if min_len > 0 else 0

            smt = timer()
            self.progress.emit(f"Similarity matrix created in {smt - start:.2f} seconds.")

            # Function to create clusters
            def create_clusters(similarity_matrix, threshold):
                try:
                    n = len(similarity_matrix)
                    clusters = [[] for _ in range(n)]
                    cluster_id = 0
                    visited = [False] * n

                    def dfs(node, cluster_id):
                        stack = [node]
                        while stack:
                            current = stack.pop()
                            if not visited[current]:
                                visited[current] = True
                                clusters[current].append(cluster_id)
                                for neighbor in range(n):
                                    if similarity_matrix[current, neighbor] > threshold and not visited[neighbor]:
                                        stack.append(neighbor)

                    for i in range(n):
                        if not visited[i]:
                            if any(similarity_matrix[i, j] > threshold for j in range(n) if i != j):
                                dfs(i, cluster_id)
                                cluster_id += 1
                    return clusters
                except Exception as e:
                    self.progress.emit(f"Error during cluster creation: {e}")
                    return []

            # Create clusters
            clusters = create_clusters(similarity_matrix, self.threshold)
            cet = timer()
            self.progress.emit(f"Clustering completed in {cet - smt:.2f} seconds.")

            # Save clusters to the output CSV file
            try:
                with open(self.output_file, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    header = ["dc.title", "Cluster IDs"]
                    writer.writerow(header)
                    for i in range(len(data)):
                        row = [data[i], ", ".join(map(str, clusters[i])) if clusters[i] else ""]
                        writer.writerow(row)
            except Exception as e:
                self.progress.emit(f"Error writing output file: {e}")
                print(e)
                return

            end = timer()
            self.progress.emit(f"Clusters saved as '{self.output_file}' in {end - cet:.2f} seconds.")
            self.progress.emit(f"Total program took {end - start:.2f} seconds.")
        except Exception as e:
            self.progress.emit(f"An unexpected error occurred: {e}")
            print(e)


# Define another window
class SecondWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Canvas: Data Analysis Window")
        self.setGeometry(100, 100, 800, 600)

        # Main layout
        main_layout = QVBoxLayout()

        # Input threshold layout
        threshold_layout = QHBoxLayout()
        self.threshold_input = QLineEdit(self)
        self.threshold_input.setPlaceholderText("Enter threshold (e.g., 20)")
        self.threshold_input.setStyleSheet("padding: 5px; font-size: 14px;")  # Slight padding for input box
        threshold_label = QLabel("Threshold:")
        threshold_label.setStyleSheet("font-size: 16px; font-weight: bold;")  # Label styling
        threshold_layout.addWidget(threshold_label)
        threshold_layout.addWidget(self.threshold_input)
        main_layout.addLayout(threshold_layout)

        # Input file selection button
        input_layout = QHBoxLayout()
        self.input_button = QPushButton("Choose Input File", self)
        self.input_button.setStyleSheet(self.get_button_style())
        self.input_button.clicked.connect(self.choose_input_file)
        input_layout.addWidget(self.input_button)
        self.input_label = QLabel("No file selected")
        input_layout.addWidget(self.input_label)
        main_layout.addLayout(input_layout)

        # Output file selection button
        output_layout = QHBoxLayout()
        self.output_button = QPushButton("Choose Output File", self)
        self.output_button.setStyleSheet(self.get_button_style())
        self.output_button.clicked.connect(self.choose_output_file)
        output_layout.addWidget(self.output_button)
        self.output_label = QLabel("No file selected")
        output_layout.addWidget(self.output_label)
        main_layout.addLayout(output_layout)

        # Clustering buttons
        button_layout = QHBoxLayout()
        self.edit_btn = QPushButton("Edit Clustering", self)
        self.edit_btn.setStyleSheet(self.get_button_style())
        self.lcs_btn = QPushButton("LCS Clustering", self)
        self.lcs_btn.setStyleSheet(self.get_button_style())
        self.lcss_btn = QPushButton("LCSS Clustering", self)
        self.lcss_btn.setStyleSheet(self.get_button_style())
        self.lcss_btn.clicked.connect(self.run_clustering)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.lcs_btn)
        button_layout.addWidget(self.lcss_btn)
        main_layout.addLayout(button_layout)

        # Status label
        self.status_label = QLabel("Ready", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px; margin-top: 20px; font-weight: bold; color: green;")
        main_layout.addWidget(self.status_label)

        self.setLayout(main_layout)

        # Store file paths
        self.input_file = ""
        self.output_file = ""

    def get_button_style(self):
        return """
        QPushButton {
            background-color: #3498db;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        """

    def choose_input_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Input CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            self.input_file = file_name
            self.input_label.setText(file_name.split('/')[-1])  # Show only the file name, not the full path

    def choose_output_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Select Output CSV File", "", "CSV Files (*.csv);;All Files (*)", options=options)
        if file_name:
            self.output_file = file_name
            self.output_label.setText(file_name.split('/')[-1])  # Show only the file name, not the full path

    def run_clustering(self):
        if not self.input_file or not self.output_file:
            self.status_label.setText("Please select both input and output files.")
            return

        try:
            threshold = float(self.threshold_input.text())
        except ValueError:
            self.status_label.setText("Please enter a valid numeric threshold.")
            return

        self.status_label.setText("Processing...")
        self.worker = ClusteringWorker(self.input_file, self.output_file, threshold)
        self.worker.progress.connect(self.show_progress)
        self.worker.start()

    def show_progress(self, message):
        self.status_label.setText(message)

# Define the main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Canvas ADCT")
        self.setGeometry(50, 50, 900, 700)

        # Create the stacked widget
        self.stacked_widget = QStackedWidget()

        # Create instances of your windows
        self.adct_window = ADCTWindow()
        self.second_window = SecondWindow()

        # Add the windows to the stacked widget
        self.stacked_widget.addWidget(self.adct_window)
        self.stacked_widget.addWidget(self.second_window)

        # Set the central widget of the main window to the stacked widget
        self.setCentralWidget(self.stacked_widget)

        # Create actions to switch windows
        switch_to_adct_action = QAction("Canvas Graph Window", self)
        switch_to_adct_action.triggered.connect(self.switch_to_adct)

        switch_to_second_window_action = QAction("Canvas: Data Analysis Window", self)
        switch_to_second_window_action.triggered.connect(self.switch_to_second_window)

        # Add the actions to the menu bar
        menubar = self.menuBar()
        view_menu = menubar.addMenu("Switch")
        view_menu.addAction(switch_to_adct_action)
        view_menu.addAction(switch_to_second_window_action)

    def switch_to_adct(self):
        self.stacked_widget.setCurrentWidget(self.adct_window)

    def switch_to_second_window(self):
        self.stacked_widget.setCurrentWidget(self.second_window)


# Main function to run the application
if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec_())
