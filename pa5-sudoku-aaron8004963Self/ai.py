from __future__ import print_function
from game import sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random, copy

class AI:
    def __init__(self):
        pass

    def solve(self, problem):
        domains = init_domains()
        restrict_domain(domains, problem) 

        # TODO: implement backtracking search. 

        # # TODO: delete this block ->
        # # Note that the display and test functions in the main file take domains as inputs. 
        # #   So when returning the final solution, make sure to take your assignment function 
        # #   and turn the value into a single element list and return them as a domain map. 
        # for spot in sd_spots:
        #     domains[spot] = [1]
        # return domains
        # # <- TODO: delete this block
        assignment = {'C': False}  ##Assignment function
        decisions = [] ##Decision stack
 

        # TODO: implement backtracking search. 

        while True:
            assignment, domains = self.propagate(assignment, domains) # Propagate using arc-consistency
            if not assignment['C']:
                if len(assignment) == (len(sd_spots) + 1): # Check if all variables are assigned
                    return domains # Solved, return the full assignment in solution format
                else:
                    spot = self.make_decision(assignment, domains) # Assign some value to an unassigned variable
                    if spot is not None:  # Ensuring a spot was chosen
                        decisions.append([copy.deepcopy(assignment), spot, copy.deepcopy(domains)])   
            else:
                if not decisions:
                    return None
                else:
                    assignment, domains = self.backtrack(decisions)
                    assignment['C'] = False 
                

    # TODO: add any supporting function you need
    def propagate(self, assignment, domains):
        while True:

            for spot in domains.keys():
                if len(domains[spot]) == 1 and  (spot not in assignment):
                    assignment[spot] = domains[spot][0]
            
            for spot in assignment:
                if spot != "C":
                    domains[spot] = [assignment[spot]]
            
            for spot in domains.keys():
                if len(domains[spot]) == 0:
                    assignment["C"] = 1
                    return assignment, domains
                     
            conflict, domains = self.check_and_resolve_conflicts(domains)            
            if not conflict:
                return assignment, domains
            
    def check_and_resolve_conflicts(self,domains):
        conflict = False

        for spot in sd_spots:
            if len(domains[spot]) > 1:  
                peers_with_singleton_domains = [c for c in sd_peers[spot] if len(domains[c]) == 1]
                current_domain_set = set(domains[spot])  

                for peer in peers_with_singleton_domains:
                    value = domains[peer][0]
                    if value in current_domain_set:
                        current_domain_set.remove(value)
                        conflict = True

                domains[spot] = list(current_domain_set)  

        return conflict, domains
    
    def make_decision(self, assignment, domains):
        for spot in sd_spots:  
            if spot not in assignment:  
                if len(domains[spot]) > 0:  # Ensure there is at least one possible value
                    assignment[spot] = domains[spot][0]  
                    return spot  
        return None

    def backtrack(self, decisions):
        assignment, spot, domains = decisions.pop()

        if spot in assignment:
            value = assignment[spot]
            
            assignment.pop(spot, None)

            if value in domains[spot]:
                domains[spot].remove(value)

        return assignment, domains

    #### The following templates are only useful for the EC part #####

    # EC: parses "problem" into a SAT problem
    # of input form to the program 'picoSAT';
    # returns a string usable as input to picoSAT
    # (do not write to file)
    def sat_encode(self, problem):
        text = ""

        # TODO: write CNF specifications to 'text'

        return text

    # EC: takes as input the dictionary mapping 
    # from variables to T/F assignments solved for by picoSAT;
    # returns a domain dictionary of the same form 
    # as returned by solve()
    def sat_decode(self, assignments):
        # TODO: decode 'assignments' into domains
        
        # TODO: delete this ->
        domains = {}
        for spot in sd_spots:
            domains[spot] = [1]
        return domains
        # <- TODO: delete this
