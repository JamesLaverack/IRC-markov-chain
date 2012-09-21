import collections


if __name__ == "__main__":
    # Create a dictionary of a dictionarry of counters. Such that 
    # token_counters['black_knight']['flesh']['wound'] is the number of times
    # that the word 'python' follows the word 'monty' in lines posted by the
    # user 'black_knight'
    token_counters = collections.defaultdict(lambda : collections.defaultdict(collections.Counter))
    
    print token_counters['black_knight']['flesh']['wound']
    token_counters['black_knight']['flesh']['wound']+=1
    print token_counters['black_knight']['flesh']['wound']