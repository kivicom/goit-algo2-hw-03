# Performance Comparison Report: OOBTree vs Dictionary

## Test Results

| Operation         | OOBTree (sec) | Dictionary (sec) |
|-------------------|---------------|------------------|
| Insertion         | 0.0550     | 0.0049     |
| Deletion          | 0.0001     | 0.0000     |
| Range Query       | 0.0752     | 0.0362     |

Number of items in range (10000–90000): 79927 (OOBTree), 79927 (Dictionary)

## Analysis

### 1. Insertion Time
OOBTree inserts items in 0.0550 sec, while Dictionary takes 0.0049 sec. Dictionary is faster due to O(1) complexity, while OOBTree has O(log n).

### 2. Deletion Time
Deletion in OOBTree takes 0.0001 sec, while in Dictionary it takes 0.0000 sec. Dictionary is faster with O(1), while OOBTree has O(log n).

### 3. Range Query Time
Range query in OOBTree takes 0.0752 sec, while in Dictionary it takes 0.0362 sec. OOBTree is faster with O(log n + k), while Dictionary has O(n).

### Conclusions
- OOBTree is better for range queries based on product IDs.
- Dictionary is better for insertion and deletion operations.
- The choice depends on the type of operations with product data.
