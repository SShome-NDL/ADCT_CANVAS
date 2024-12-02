import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QPushButton, QVBoxLayout, QAction, \
    QFileDialog, QLabel, QLineEdit, QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, Qt
import numpy as np
import pandas as pd
import csv
from timeit import default_timer as timer

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

            # Modified LCS function to return the matching part (substring) and its length
            def lcs_starting_from_first(str1, str2):
                matching_part = []
                for c1, c2 in zip(str1, str2):
                    if c1 == c2:
                        matching_part.append(c1)
                    else:
                        break
                return len(matching_part), ''.join(matching_part)

            # Read data from the input CSV file
            try:
                data = pd.read_csv(self.input_file)
                data = data['dc.title']
            except Exception as e:
                self.progress.emit(f"Error reading input file: {e}")
                return

            # Create the similarity matrix and store matching parts
            n = len(data)
            similarity_matrix = np.zeros((n, n))
            matching_parts = [[''] * n for _ in range(n)]  # To store the matching substrings

            for i in range(n):
                for j in range(n):
                    if i < j:
                        lcs_length, matching_part = lcs_starting_from_first(data[i], data[j])
                        min_len = max(len(data[i]), len(data[j]))
                        similarity_matrix[i, j] = (lcs_length / min_len * 100) if min_len > 0 else 0
                        matching_parts[i][j] = matching_part

            smt = timer()
            self.progress.emit(f"Similarity matrix created in {smt - start:.2f} seconds.")

            # Function to create clusters and track the matching parts of clusters
            def create_clusters(similarity_matrix, threshold):
                try:
                    n = len(similarity_matrix)
                    clusters = [[] for _ in range(n)]
                    cluster_id = 0
                    visited = [False] * n
                    cluster_matching_parts = [[] for _ in range(n)]  # Store the matching parts for each cluster

                    def dfs(node, cluster_id):
                        stack = [node]
                        while stack:
                            current = stack.pop()
                            if not visited[current]:
                                visited[current] = True
                                clusters[current].append(cluster_id)
                                cluster_matching_parts[current] = []  # Reset matching parts for the current cluster
                                for neighbor in range(n):
                                    if similarity_matrix[current, neighbor] > threshold and not visited[neighbor]:
                                        stack.append(neighbor)
                                        # Store the matching part that caused clustering
                                        cluster_matching_parts[current].append(matching_parts[current][neighbor])

                    for i in range(n):
                        if not visited[i]:
                            if any(similarity_matrix[i, j] > threshold for j in range(n) if i != j):
                                dfs(i, cluster_id)
                                cluster_id += 1
                    return clusters, cluster_matching_parts
                except Exception as e:
                    self.progress.emit(f"Error during cluster creation: {e}")
                    return [], []

            # Create clusters and get the matching parts for each cluster
            clusters, cluster_matching_parts = create_clusters(similarity_matrix, self.threshold)
            cet = timer()
            self.progress.emit(f"Clustering completed in {cet - smt:.2f} seconds.")

            # Function to find the most common matching part or ensure unique matching part in a cluster
            def get_common_matching_part(matching_parts_list):
                if not matching_parts_list:
                    return ""
                # Remove empty parts
                filtered_parts = [part for part in matching_parts_list if part]
                if not filtered_parts:
                    return ""
                # If all parts are the same, return that part
                if all(part == filtered_parts[0] for part in filtered_parts):
                    return filtered_parts[0]
                # Otherwise, find the most common part
                from collections import Counter
                common_part = Counter(filtered_parts).most_common(1)[0][0]
                return common_part

            # Save clusters to the output CSV file with the matching part
            try:
                with open(self.output_file, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    header = ["dc.title", "Cluster IDs", "Matching Part"]
                    writer.writerow(header)
                    for i in range(len(data)):
                        cluster_ids = ", ".join(map(str, clusters[i])) if clusters[i] else ""
                        # Get the common matching part for the cluster
                        matching_part = get_common_matching_part(cluster_matching_parts[i])
                        row = [data[i], cluster_ids, matching_part]
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

            # Modified LCS function to return the matching part (substring) and its length
            def lcs_starting_from_first(str1, str2):
                matching_part = []
                for c1, c2 in zip(str1, str2):
                    if c1 == c2:
                        matching_part.append(c1)
                    else:
                        break
                return len(matching_part), ''.join(matching_part)

            # Read data from the input CSV file
            try:
                data = pd.read_csv(self.input_file)
                data = data['dc.title']
            except Exception as e:
                self.progress.emit(f"Error reading input file: {e}")
                return

            # Create the similarity matrix and store matching parts
            n = len(data)
            similarity_matrix = np.zeros((n, n))
            matching_parts = [[''] * n for _ in range(n)]  # To store the matching substrings

            for i in range(n):
                for j in range(n):
                    if i < j:
                        lcs_length, matching_part = lcs_starting_from_first(data[i], data[j])
                        min_len = max(len(data[i]), len(data[j]))
                        similarity_matrix[i, j] = (lcs_length / min_len * 100) if min_len > 0 else 0
                        matching_parts[i][j] = matching_part

            smt = timer()
            self.progress.emit(f"Similarity matrix created in {smt - start:.2f} seconds.")

            # Function to create clusters and track the matching parts of clusters
            def create_clusters(similarity_matrix, threshold):
                try:
                    n = len(similarity_matrix)
                    clusters = [[] for _ in range(n)]
                    cluster_id = 0
                    visited = [False] * n
                    cluster_matching_parts = [[] for _ in range(n)]  # Store the matching parts for each cluster

                    def dfs(node, cluster_id):
                        stack = [node]
                        while stack:
                            current = stack.pop()
                            if not visited[current]:
                                visited[current] = True
                                clusters[current].append(cluster_id)
                                cluster_matching_parts[current] = []  # Reset matching parts for the current cluster
                                for neighbor in range(n):
                                    if similarity_matrix[current, neighbor] > threshold and not visited[neighbor]:
                                        stack.append(neighbor)
                                        # Store the matching part that caused clustering
                                        cluster_matching_parts[current].append(matching_parts[current][neighbor])

                    for i in range(n):
                        if not visited[i]:
                            if any(similarity_matrix[i, j] > threshold for j in range(n) if i != j):
                                dfs(i, cluster_id)
                                cluster_id += 1
                    return clusters, cluster_matching_parts
                except Exception as e:
                    self.progress.emit(f"Error during cluster creation: {e}")
                    return [], []

            # Create clusters and get the matching parts for each cluster
            clusters, cluster_matching_parts = create_clusters(similarity_matrix, self.threshold)
            cet = timer()
            self.progress.emit(f"Clustering completed in {cet - smt:.2f} seconds.")

            # Function to find the common matching part for each cluster
            def get_common_matching_part(matching_parts_list):
                if not matching_parts_list:
                    return ""
                # Remove empty parts
                filtered_parts = [part for part in matching_parts_list if part]
                if not filtered_parts:
                    return ""
                # If all parts are the same, return that part
                if all(part == filtered_parts[0] for part in filtered_parts):
                    return filtered_parts[0]
                # Otherwise, find the most common part
                from collections import Counter
                common_part = Counter(filtered_parts).most_common(1)[0][0]
                return common_part

            # Map each cluster to its common matching part
            cluster_matching_part_map = {}
            for cluster_id in range(max(max(clusters, default=[-1])) + 1):
                matching_parts_in_cluster = [
                    part
                    for idx, cluster in enumerate(clusters)
                    if cluster and cluster[0] == cluster_id
                    for part in cluster_matching_parts[idx]
                ]
                common_matching_part = get_common_matching_part(matching_parts_in_cluster)
                cluster_matching_part_map[cluster_id] = common_matching_part

            # Save clusters to the output CSV file with the matching part for each element
            try:
                with open(self.output_file, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    header = ["dc.title", "Cluster IDs", "Matching Segment"]
                    writer.writerow(header)
                    for i in range(len(data)):
                        cluster_ids = ", ".join(map(str, clusters[i])) if clusters[i] else ""
                        # Get the common matching part for the current element's cluster
                        if clusters[i]:
                            common_matching_part = cluster_matching_part_map[clusters[i][0]]
                        else:
                            common_matching_part = ""
                        row = [data[i], cluster_ids, common_matching_part]
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
