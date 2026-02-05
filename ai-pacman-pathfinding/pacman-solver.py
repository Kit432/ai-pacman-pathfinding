#!/usr/bin/env python3
""" ----------------------------------------------------------------------------
******** Κώδικας για DFS και άλλες μεθόδους αναζήτησης
******** (επέκταση μετώπου και διαχείριση ουράς)
******** Συγγραφέας: Λιν Χονγκ Τσε 21390120
"""
import random

import copy

import sys 
sys.setrecursionlimit(10**6) 

# Σταθερή τυχαία τιμή Global seed
GLOBAL_SEED = random.random()

"""Βοηθητική συνάρτηση που βρίσκει τη θέση του Pacman στην πίστα."""
def find_pacman(state):
    for i in range(len(state)):
        if state[i][0] == 'p':
            return i
    return -1  # Pacman δεν βρέθηκε, κάτι πήγε λάθος



"""Τελεστές Μετάβασης: move left, move right, eat fruit, destroy fruit"""

"""Μετακινεί τον Pacman ένα κελί αριστερά αν είναι εφικτό."""
def move_left(state):
    pac_pos = find_pacman(state)  # Βρίσκουμε τη θέση του Pacman
    if pac_pos > 0:  # Αν δεν είναι στο πρώτο κελί
        state[pac_pos][0] = ' '
        # Ανταλλάσσουμε τις θέσεις του Pacman
        state[pac_pos-1][0] = 'p'
        return state
    else:
	    return None  # Δεν μπορεί να κινηθεί αριστερά
    
"""Μετακινεί τον Pacman ένα κελί δεξιά αν είναι εφικτό."""
def move_right(state):
    pac_pos = find_pacman(state)  # Βρίσκουμε τη θέση του Pacman
    if pac_pos < len(state)-1:  # Αν δεν είναι στο τελευταίο κελί
        state[pac_pos][0] = ' '
        # Ανταλλάσσουμε τις θέσεις του Pacman
        state[pac_pos+1][0] = 'p'
        return state
    else:
        return None  # Δεν μπορεί να κινηθεί δεξιά

"""Ο Pacman τρώει το φαγώσιμο φρούτο αν βρίσκεται στο ίδιο κελί."""
def eat_fruit(state):
    pac_pos = find_pacman(state)
    if state[pac_pos][1] == 'f':  # Αν υπάρχει φαγώσιμο φρούτο στο κελί του Pacman
        state[pac_pos][1] = ' '  # Αφαιρούμε το φρούτο
        return state
    else:
	    return None  # Δεν υπάρχει φρούτο για να φάει

"""Ο Pacman καταστρέφει το δηλητηριώδες φρούτο και δημιουργεί νέο φαγώσιμο φρούτο."""
def destroy_poison(state):
    pac_pos = find_pacman(state)
    if state[pac_pos][1] == 'd':  # Αν υπάρχει δηλητηριώδες φρούτο στο κελί του Pacman
        state[pac_pos][1] = ' '  # Καταστρέφουμε το δηλητηριώδες φρούτο
        
        # Βρίσκουμε τυχαίο κενό κελί χωρίς τον Pacman για να τοποθετήσουμε το νέο φαγώσιμο φρούτο
        random.seed(GLOBAL_SEED)
        empty_cells = [i for i in range(len(state)) if state[i][0] != 'p' and state[i][1] == ' ']
        if empty_cells:
            new_fruit_pos = random.choice(empty_cells)  # Τυχαία επιλογή κενού κελιού
            # Κάναμε import random στην αρχή
            state[new_fruit_pos][1] = 'f'  # Τοποθετούμε το νέο φρούτο
        return state
    else:
	    return None  # Δεν υπάρχει δηλητηριώδες φρούτο να καταστραφεί



"""Επιστρέφει όλες τις έγκυρες επόμενες καταστάσεις (απογόνους) από την τρέχουσα κατάσταση."""
def find_children(state):
    children = []
    
    # Δοκιμάζουμε την κίνηση αριστερά
    left_state=copy.deepcopy(state)
    child_left = move_left(left_state)
    if not child_left==None:
        children.append(child_left)
    """ Η copy.deepcopy χρησιμοποιείται για να διασφαλίσει ότι κάθε νέα κατάσταση (child) είναι μια ανεξάρτητη αντιγραφή της τρέχουσας. 
        Κάθε ενέργεια (move_left, move_right, κ.λπ.) αλλάζει τον πίνακα state. Χωρίς deepcopy, όλες οι καταστάσεις θα δείχνουν στην ίδια μνήμη, με αποτέλεσμα να μην είναι σαφής η διαφοροποίηση μεταξύ τους.
    """
    # Δοκιμάζουμε την κίνηση δεξιά
    right_state=copy.deepcopy(state)
    child_right = move_right(right_state)
    if not child_right==None:
        children.append(child_right)
    
    # Δοκιμάζουμε το φάγωμα φρούτου
    eat_state=copy.deepcopy(state)
    child_eat = eat_fruit(eat_state)
    if not child_eat==None:
        children.append(child_eat)
    
    # Δοκιμάζουμε την καταστροφή δηλητηριώδους φρούτου
    destroy_state=copy.deepcopy(state)
    child_destroy = destroy_poison(destroy_state)
    if not child_destroy==None:
        children.append(child_destroy)
    
    return children  # Επιστρέφουμε τη λίστα με όλες τις έγκυρες καταστάσεις



"""Ελέγχει αν η τρέχουσα κατάσταση είναι η τελική κατάσταση (στόχος)."""
def is_goal_state(state):
    # Μετράει πόσα κελιά περιέχουν Pacman
    pacman_count = 0
    
    for cell in state:
        pacman, fruit = cell
        # Ελέγχει αν υπάρχουν φρούτα(φαγώσιμα ή δηλητηριώδες)
        if fruit in ['f', 'd']:
            return False
        # Μετράει πόσες φορές εμφανίζεται ο Pacman
        if pacman == 'p':
            pacman_count += 1
    
    # Ο Pacman θα πρέπει να εμφανίζεται ακριβώς μία φορά
    return pacman_count == 1



"""" ----------------------------------------------------------------------------
** Αναπαράσταση Αποτελεσμάτων
"""
def print_state(state):
    visual = []
    for cell in state:
        pacman = 'P' if cell[0] == 'p' else '.'  # Αν υπάρχει ο pacman
        fruit = 'F' if cell[1] == 'f' else 'D' if cell[1] == 'd' else '.'  # Αν υπάρχει φρούτο
        if pacman == 'P' and fruit != '.':
            visual.append(f'{pacman}+{fruit}')  # Pacman με φρούτο
        elif pacman == 'P':
            visual.append(pacman)  # Pacman μόνος του
        elif fruit != '.':
            visual.append(fruit)  # Φρούτο μόνο του
        else:
            visual.append('.')  # Κενό κελ
        
    print(' | '.join(visual))  # Εμφανίζει την πίστα

       
def print_queue(queue):
    for i, path in enumerate(queue):
            print(f"\nPath {i + 1}:")
            for state in path:
                print_state(state)  # Χρησιμοποιεί την print_state() που φτιάξαμε πριν



""" ----------------------------------------------------------------------------
** Αρχικοποίηση Μετώπου
"""

def make_front(state):
    return [state]  # Το μέτωπο είναι λίστα με τις καταστάσεις προς ανάλυση
    
""" ----------------------------------------------------------------------------
**** Επέκταση Μετώπου    
"""

def expand_front(front, method):  
    if method=='DFS':        
        if front:
            print("Front states:")
            for state in front:
                print_state(state)
            node=front.pop(0)   # Αφαιρούμε τον πρώτο κόμβο από το μέτωπο
            for child in find_children(node):   # Εύρεση των παιδιών (απογόνων) της κατάστασης  
                front.insert(0,child)   # Προσθέτουμε τα παιδιά στην ΑΡΧΗ του μετώπου
    
    elif method=='BFS':
        if front:
            print("Front states:")
            for state in front:
                print_state(state)
            node=front.pop(0)
            for child in find_children(node):
                front.append(child)     # Προσθέτουμε τα παιδιά στο ΤΕΛΟΣ του μετώπου

    elif method=='BestFS':
        if front:
            print("Front states")
            for state in front:
                print_state(state)
                print(f"Heuristic: {heuristic(state)}\n")   # Τυπώνει την τιμή του ευριστικού κριτηρίου για κάθε κατάσταση
            node=front.pop(0)
            for child in find_children(node):
                front.append(child)     # Προσθέτουμε τα παιδιά στο μέτωπο
                front.sort(key=lambda state: heuristic(state))      # Ταξινομούμε το μέτωπο με βάση το ευριστικό κριτήριο 
                                                                    # (όσο μικρότερο τόσο πιο μπροστά στο μέτωπο τοποθετείται | αν καταστάσεις έχουν την ίδια ευριστική τιμή, διατηρούμε τη σειρά εισαγωγής τους)
         
    return front



""" ----------------------------------------------------------------------------
**** QUEUE
**** Διαχείριση ουράς
"""

""" ----------------------------------------------------------------------------
** initialization of queue
** Αρχικοποίηση ουράς
"""

def make_queue(state):
    return [[state]]    #Η ουρά είναι λίστα από κάθε μονοπάτι

""" ----------------------------------------------------------------------------
**** expanding queue
**** επέκταση ουράς
"""

def extend_queue(queue, method):
    if method=='DFS':
        node=queue.pop(0)
        for child in find_children(node[-1]): # Εύρεση των παιδιών (απογόνων) της τελευταίας κατάστασης κάθε μονοπατιού
            path=copy.deepcopy(node)
            path.append(child)
            queue.insert(0,path)    # Προσθέτουμε τα νέα μονοπάτια στην ΑΡΧΗ του συνόλου
    
    elif method=='BFS':
        node=queue.pop(0)
        for child in find_children(node[-1]):
            path=copy.deepcopy(node)
            path.append(child)
            queue.append(path)  # Προσθέτουμε τα νέα μονοπάτια στο ΤΕΛΟΣ του συνόλου

    elif method=='BestFS':
        node = queue.pop(0)
        for child in find_children(node[-1]):
            path=copy.deepcopy(node)
            path.append(child)
            queue.append(path)
            queue.sort(key=lambda path: heuristic(path[-1]))    # Ταξινομούμε με βάση τις 
            # τελευταίες καταστάσεις του κάθε μονοπατιού με βάση το ευριστικό κριτήριο 
    
    print("\nQueue after expansion:")
    print_queue(queue)

    return queue



""" ----------------------------------------------------------------------------
**** Συνάρτηση Ευριστικού Κριτηρίου Αναζήτησης
"""
def heuristic(state):
    pacman_pos = None   # Θέση του Pacman
    poison_pos = None   # Θέση του δηλητηριώδες φρούτου
    fruit_positions = []    # Θέση όλων των φαγώσιμων φρούτων

    # Βρίσκουμε τις θέσεις όλων των αντικειμένων
    for i in range(len(state)):
        if state[i][0] == 'p':
            pacman_pos = i
        if state[i][1] == 'd':
            poison_pos = i
        if state[i][1] == 'f':
            fruit_positions.append(i)

    # Αν υπάρχει το δηλητηριώδες φρούτο, δώσε προτεραιότητα στο να το καταστρέψεις
    if not poison_pos==None:
        return 13 + abs(pacman_pos - poison_pos) # Θέλουμε να κατστρέψουμε το δηλητηριώδες φρούτο πρώτα απ'όλα.
                                                 # Έτσι θα θεωρήσουμε κάθε κατάσταση χωρίς το δηλητηριώδες φρούτο
                                                 # ως πιο κοντά στο στόχο μας από οποιαδήποτε κατάσταση με το 
                                                 # δηλητηριώδες φρούτο. Στην χειρότερη περίπτωση μπορούμε να βρεθούμε
                                                 # στην κατάσταση P| | |F|F|F που επιστρέφει 3+4+5=12. Γι'αυτόν τον
                                                 # λόγο αν υπάρχει δηλητηριώδες φρούτο επιστρέφεται η απόσταση του
                                                 # Pacman από αυτό + 13.
    else:
    # Αν δεν υπάρχει το δηλητηριώδες φρούτο, μέτρα την συνολική απόσταση από όλα τα φρούτα
        total_distance = 0
        for fruit_pos in fruit_positions:
            total_distance += abs(pacman_pos - fruit_pos)
        return total_distance  # Lower distance means closer to the goal



""" ----------------------------------------------------------------------------
**** Βασική αναδρομική συνάρτηση για δημιουργία δέντρου αναζήτησης (αναδρομική επέκταση δέντρου)
"""
def find_solution(front, closed, method, step=0):
    if not front:  # Αν το μέτωπο είναι κενό, δεν βρέθηκε λύση
        print('No solution')
    
    elif front[0] in closed:  # Αν η πρώτη κατάσταση έχει ήδη εξεταστεί
        print("Step:", step)
        print("State Removed:")
        print_state(front[0])
        new_front = copy.deepcopy(front)
        new_front.pop(0)  # Αφαιρούμε την τρέχουσα κατάσταση και συνεχίζουμε
        find_solution(new_front, closed, method, step+1)
    
    elif is_goal_state(front[0]):  # Αν η τρέχουσα κατάσταση είναι ο στόχος
        print('Goal found in', step, 'steps!')
        print("Final State:")
        print_state(front[0])  # Εμφανίζει την τελική κατάσταση της πίστας
    
    else:
        print("Step:", step)
        closed.append(front[0])  # Προσθέτουμε την κατάσταση στη λίστα των εξετασμένων
        front_copy = copy.deepcopy(front)
        front_children = expand_front(front_copy, method)
        print("Current State:")
        print_state(front[0])  # Εμφανίζει την τρέχουσα κατάσταση της πίστας
        closed_copy = copy.deepcopy(closed)
        find_solution(front_children, closed_copy, method, step+1)



""" ----------------------------------------------------------------------------
**** Βασική αναδρομική συνάρτηση για δημιουργία δέντρου αναζήτησης (αναδρομική επέκταση δέντρου) με διαχείριση ουράς
"""
def find_solution_with_queue(front, queue, closed, method, step=0):
    if not front:  # Αν το μέτωπο είναι κενό, δεν βρέθηκε λύση
        print('No solution')
    
    elif front[0] in closed:  # Αν η πρώτη κατάσταση έχει ήδη εξεταστεί
        print("Step:", step)
        print("State Removed:")
        print_state(front[0])
        new_front = copy.deepcopy(front)
        new_front.pop(0)  # Αφαιρούμε την τρέχουσα κατάσταση και συνεχίζουμε
        new_queue = copy.deepcopy(queue)
        new_queue.pop(0)
        find_solution_with_queue(new_front, new_queue, closed, method, step+1)
    
    elif is_goal_state(front[0]):  # Αν η τρέχουσα κατάσταση είναι ο στόχος
        print('Goal found in', step, 'steps!')
        print("Final State:")
        print_state(front[0])  # Εμφανίζει την τελική κατάσταση της πίστας
        print("Full Path:")
        for state in queue[0]:  # Εμφανίζει ολόκληρο το μονοπάτι που μας πήγε στην τελκή κατάσταση
            print_state(state)
    
    else:
        print("\nStep:", step)
        closed.append(front[0])  # Προσθέτουμε την κατάσταση στη λίστα των εξετασμένων
        front_copy = copy.deepcopy(front)
        front_children = expand_front(front_copy, method)
        print("Current State:")
        print_state(front[0])  # Εμφανίζει την τρέχουσα κατάσταση της πίστας
        queue_copy = copy.deepcopy(queue)
        queue_children = extend_queue(queue_copy, method)
        closed_copy = copy.deepcopy(closed)
        find_solution_with_queue(front_children, queue_children, closed_copy, method, step+1)



""" ----------------------------------------------------------------------------
**** Συνάρτηση Μέτρησης Χρόνου Εκτέλεσης και Χρήση Μνήμης
"""
def measure_performance(method, front, closed):
    import time
    import tracemalloc

    tracemalloc.start()  # Έναρξη παρακολούθησης μνήμης
    start_time = time.time()  # Έναρξη χρονικής μέτρησης

    find_solution(front, closed, method)

    end_time = time.time()  # Τέλος χρονικής μέτρησης
    current, peak = tracemalloc.get_traced_memory()  # Απόκτηση τρέχουσας και μέγιστης χρήσης μνήμης
    tracemalloc.stop()  # Τερματισμός παρακολούθησης μνήμης

    execution_time = end_time - start_time
    print(f"Method: {method}")
    print(f"Execution Time: {execution_time:.4f} seconds")
    print(f"Memory Usage: {peak / 10**6:.2f} MB (peak)")


"""" ----------------------------------------------------------------------------
** Κλήση Εκτέλεσης Κώδικα
"""
           
def main():

    initial_state=[[' ','d'],[' ','f'],['p',' '],[' ',' '],[' ','f'],[' ',' ']]
    
    """"
    ----------------------------------------------------------------------------
    **** Επιλογή Μεθόδου Αναζήτησης
    """
    
    print("Select the search method:")
    print("1. DFS (Depth-First Search)")
    print("2. BFS (Breadth-First Search)")
    print("3. Best-First Search")
    choice = int(input("Enter your choice (1, 2, or 3): "))
    
    if choice not in [1, 2, 3]:
        print("Invalid choice. Exiting program.")
        return
    
    methods = {1: 'DFS', 2: 'BFS', 3: 'BestFS'}
    method = methods[choice]

    """"
    ----------------------------------------------------------------------------
    **** Χρήση Ουράς ή Όχι
    """
    
    print("Use queue-based approach?")
    print("1. Yes")
    print("2. No")
    queue_choice = int(input("Enter your choice (1, 2): "))

    """"
    ----------------------------------------------------------------------------
    **** Έναρξη Αναζήτησης
    """
    

    print('Begin Searching:')

    if queue_choice==1:
        print(f"Using {method} with Queue.")
        find_solution_with_queue(make_front(initial_state), make_queue(initial_state), [], method)
    else:
        print(f"Using {method} with Front.")
        find_solution(make_front(initial_state), [], method)


    """"
    ----------------------------------------------------------------------------
    **** Εξέταση Χρόνου Εκτέλεσης και Χρήση Μνήμης
    """
    #initial_state_1 = [[' ','d'],[' ','f'],['p',' '],[' ',' '],[' ','f'],[' ',' ']]
    #initial_state_2 = [[' ','d'],['p',' '],[' ',' '],[' ',' '],[' ','f'],[' ','f']]
    #initial_state_3 = [['p',' '],[' ','f'],[' ',' '],[' ','f'],[' ',' '],[' ','d']]

    #print("Αρχική Κατάσταση 1:")
    #measure_performance('DFS', make_front(initial_state_1), [])
    #measure_performance('BFS', make_front(initial_state_1), [])
    #measure_performance('BestFS', make_front(initial_state_1), [])

    #print("Αρχική Κατάσταση 2:")
    #measure_performance('DFS', make_front(initial_state_2), [])
    #measure_performance('BFS', make_front(initial_state_2), [])
    #measure_performance('BestFS', make_front(initial_state_2), [])

    #print("Αρχική Κατάσταση 3:")
    #measure_performance('DFS', make_front(initial_state_3), [])
    #measure_performance('BFS', make_front(initial_state_3), [])
    #measure_performance('BestFS', make_front(initial_state_3), [])


if __name__ == "__main__":
    main()