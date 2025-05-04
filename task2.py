import random
import time
import csv
from BTrees.OOBTree import OOBTree
import sys

# Increase recursion limit for BTrees to handle larger datasets
sys.setrecursionlimit(10000)

# Load data from CSV file
def load_data(filename):
    data = []
    with open(filename, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append((int(row['ID']), {'Name': row['Name'], 'Category': row['Category'], 'Price': float(row['Price'])}))
    return data

# Test insertion performance
def test_insert(data, structure_type):
    start_time = time.time()
    if structure_type == "OOBTree":
        structure = OOBTree()
        for key, value in data:
            structure[key] = value
    else:
        structure = {}
        for key, value in data:
            structure[key] = value
    return time.time() - start_time, structure

# Test deletion performance
def test_delete(structure, keys_to_delete, structure_type):
    start_time = time.time()
    for key in keys_to_delete:
        if structure_type == "OOBTree":
            if key in structure:
                del structure[key]
        else:
            structure.pop(key, None)
    return time.time() - start_time

# Test range query performance
def test_range_query(structure, start, end, structure_type):
    start_time = time.time()
    if structure_type == "OOBTree":
        result = list(structure.items(min=start, max=end))
    else:
        result = [(k, v) for k, v in structure.items() if start <= k <= end]
    return time.time() - start_time, len(result)

# Generate performance report
def generate_report():
    # Configuration
    filename = 'data/generated_items_data.csv'
    delete_count = 100  # Number of items to delete
    range_start, range_end = 10000, 90000  # Range for query, adjusted to data
    
    # Load data from CSV
    data = load_data(filename)
    keys_to_delete = random.sample([item[0] for item in data], min(delete_count, len(data)))

    # Test OOBTree performance
    oobtree_insert_time, oobtree = test_insert(data, "OOBTree")
    oobtree_delete_time = test_delete(oobtree, keys_to_delete, "OOBTree")
    oobtree_range_time, oobtree_range_count = test_range_query(oobtree, range_start, range_end, "OOBTree")
    
    # Test Dictionary performance
    dict_insert_time, dictionary = test_insert(data, "Dictionary")
    dict_delete_time = test_delete(dictionary, keys_to_delete, "Dictionary")
    dict_range_time, dict_range_count = test_range_query(dictionary, range_start, range_end, "Dictionary")
    
    # Generate report in Markdown format
    report = "# Performance Comparison Report: OOBTree vs Dictionary\n\n"
    report += "## Test Results\n\n"
    report += "| Operation         | OOBTree (sec) | Dictionary (sec) |\n"
    report += "|-------------------|---------------|------------------|\n"
    report += f"| Insertion         | {oobtree_insert_time:.4f}     | {dict_insert_time:.4f}     |\n"
    report += f"| Deletion          | {oobtree_delete_time:.4f}     | {dict_delete_time:.4f}     |\n"
    report += f"| Range Query       | {oobtree_range_time:.4f}     | {dict_range_time:.4f}     |\n"
    report += f"\nNumber of items in range ({range_start}–{range_end}): {oobtree_range_count} (OOBTree), {dict_range_count} (Dictionary)\n"
    
    report += "\n## Analysis\n\n"
    report += "### 1. Insertion Time\n"
    report += f"OOBTree inserts items in {oobtree_insert_time:.4f} sec, while Dictionary takes {dict_insert_time:.4f} sec. "
    report += "Dictionary is faster due to O(1) complexity, while OOBTree has O(log n).\n\n"
    
    report += "### 2. Deletion Time\n"
    report += f"Deletion in OOBTree takes {oobtree_delete_time:.4f} sec, while in Dictionary it takes {dict_delete_time:.4f} sec. "
    report += "Dictionary is faster with O(1), while OOBTree has O(log n).\n\n"
    
    report += "### 3. Range Query Time\n"
    report += f"Range query in OOBTree takes {oobtree_range_time:.4f} sec, while in Dictionary it takes {dict_range_time:.4f} sec. "
    report += "OOBTree is faster with O(log n + k), while Dictionary has O(n).\n\n"
    
    report += "### Conclusions\n"
    report += "- OOBTree is better for range queries based on product IDs.\n"
    report += "- Dictionary is better for insertion and deletion operations.\n"
    report += "- The choice depends on the type of operations with product data.\n"
    
    return report
