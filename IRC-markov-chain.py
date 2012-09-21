import argparse
import collections
import random

# We will use integers as the hash indexes for START and END.
# These do not have to be 0 and 1, anything that's not a string
# is accepted.
Start = 0
End = 1

def random_line(username, token_counters):
    '''Given a Markov chain this will generate a sample line for a given username.'''
    current = Start
    line = "<" + username + ">"
    while current <> End:
        # chose next
        current = random.choice(list(token_counters[username][current].elements()))
        if current <> End:
            line += " " + current
    return line


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser(description='Markov-chain analysis on IRC logs.')
    parser.add_argument('filename', help='Name of a plain text IRC logfile.')
    parser.add_argument('--username',"-u", help='Give a random line only for one user.', default=None)
    parser.add_argument('--count',"-c", help='Number of lines to give for each user.', default=1, type=int)
    parser.add_argument('--breakdown',"-b", help='Breakdown of a single user\'s most common start words.', default=None)
    arguments = parser.parse_args()
    
    # Create a dictionary of a dictionarry of counters. Such that 
    # token_counters['black_knight']['flesh']['wound'] is the number of times
    # that the word 'python' follows the word 'monty' in lines posted by the
    # user 'black_knight'
    token_counters = collections.defaultdict(lambda : collections.defaultdict(collections.Counter))
    
    # Open the chatlog and read
    print "Reading chatlog..."
    logfile = open(arguments.filename, "r")
    
    # Iterate over all lines
    for line in logfile:
        if line.strip() <> '':
            # Split up into tokens, ignoring the timestamp
            tokens = line.split()[1:]
            # Only continue on pure text lines
            # TODO account for actions
            if tokens[0][0] == '<':
                # Extract name
                username = tokens[0][1:-1].replace('_','').partition('|')[0].lower()
                # Iterate over tokens
                token_counters[username][Start][tokens[1]]+=1
                for t in range(0, len(tokens[1:-1])):
                    # Incriment to say that the following word exists after this word
                    token_counters[username][tokens[t+1]][tokens[t+2]]+=1
                token_counters[username][tokens[-1]][End]+=1
    
    # Close the file
    logfile.close()
    
    # Do breakdown
    if arguments.breakdown <> None:
        print token_counters[arguments.breakdown.lower()][Start].most_common(10)
        quit()
    
    # Only print for a single user?
    if arguments.username <> None:
        for i in range(0, arguments.count):
            print random_line(arguments.username.lower(), token_counters)
        quit()
        
    # For each user make a 'most likely' sentance.
    print "Assembling most common lines..."
    for username in token_counters:
        for i in range(0, arguments.count):
            print random_line(username, token_counters)
            