#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

from collections import deque

'''This file will contain different constraint propagators to be used within
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method).
      bt_search NEEDS to know this in order to correctly restore these
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated
        constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one
        remaining variable)
        we look for unary constraints of the csp (constraints whose scope
        contains only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.


var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no
    propagation at all. Just check fully instantiated constraints'''

    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []


def FCCheck(constraint):
    un_asgn_var = constraint.get_unasgn_vars()[0]
    cur_domain = un_asgn_var.cur_domain()

    for domain_value in cur_domain:
        un_asgn_var.assign(domain_value)
        value_combination = []

        for var in constraint.get_scope():
            value_combination.append(var.get_assigned_value())

        if not constraint.check(value_combination):
            if (un_asgn_var.in_cur_domain(domain_value)) and (
                    (un_asgn_var, domain_value) not in pruned_list):
                pruned_list.append((un_asgn_var, domain_value))
                un_asgn_var.prune_value(domain_value)

        un_asgn_var.unassign()

        if un_asgn_var.cur_domain_size() == 0:
            return False

    return True


def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with
       only one uninstantiated variable. Remember to keep
       track of all pruned variable,value pairs and return '''

    global pruned_list
    pruned_list = []

    if newVar is None:
        con_lst = csp.get_all_cons()
    else:
        con_lst = csp.get_cons_with_var(newVar)

    for constraint in con_lst:
        if constraint.get_n_unasgn() == 1:
            if not FCCheck(constraint):
                return False, pruned_list

    return True, pruned_list


def GAC_Enforce(csp):
    while not len(GAC_Queue) == 0:
        constraint = GAC_Queue.popleft()
        for variable in constraint.get_scope():
            for domain_value in variable.cur_domain():
                if not constraint.has_support(variable, domain_value):
                    variable.prune_value(domain_value)
                    prune_list.append((variable, domain_value))

                    if variable.cur_domain() == []:
                        GAC_Queue.clear()
                        return False
                    else:
                        lst = csp.get_cons_with_var(variable)
                        for add_constraint in lst:
                            if add_constraint != constraint:
                                GAC_Queue.append(add_constraint)
    return True


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''

    global GAC_Queue, prune_list
    GAC_Queue = deque()
    prune_list = []

    if newVar is not None:
        lst = csp.get_cons_with_var(newVar)
        for constraint in lst:
            GAC_Queue.append(constraint)

    else:
        lst = csp.get_all_cons()
        for constraint in lst:
            GAC_Queue.append(constraint)

    if GAC_Enforce(csp) is False:
        return False, prune_list
    else:
        return True, prune_list


def ord_mrv(csp):
    ''' return variable according to the Minimum Remaining Values heuristic '''
    variable_list = csp.get_all_unasgn_vars()
    num_of_min_rem_val = float('inf')
    return_var = None

    for var in variable_list:
        if var.cur_domain_size() < num_of_min_rem_val:
            num_of_min_rem_val = var.cur_domain_size()
            return_var = var

    return return_var
