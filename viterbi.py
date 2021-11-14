def viterbi_algorithm(observations, states, start_p, trans_p, emit_p, table):
    V = [{}]
    
    # Initializes mechanism to store tracebacks and probabilities in future
    for st in states:
        V[0][st] = {"prob": start_p[st] * emit_p[st][observations[0]], "prev": None}
   
    for t in range(1, len(observations)):
        V.append({})
        for st in states:
            # Initialize - multiply by calculated probabilities of the last step and the transition probability for first state
            max_tr_prob = V[t - 1][states[0]]["prob"] * trans_p[states[0]][st]
            prev_st_selected = states[0] # Initialize variable
            for prev_st in states[1:]:
                # Find the maximum across all states by multiplying calculated probabilities by transition probability
                tr_prob = V[t - 1][prev_st]["prob"] * trans_p[prev_st][st]
                if tr_prob > max_tr_prob:
                    max_tr_prob = tr_prob # maximum probability for EACH state
                    prev_st_selected = prev_st
 
            # Multiply result by emission probability and store in V
            max_prob = max_tr_prob * emit_p[st][observations[t]]
            V[t][st] = {"prob": max_prob, "prev": prev_st_selected}
    
    if table:
        for line in dptable(V):
            print(line)
 
    opt = []
    max_prob = 0.0
    best_st = None
 
    # Traceback and find maximum probability for last state
    for st, data in V[-1].items():
        if data["prob"] > max_prob:
            max_prob = data["prob"]
            best_st = st
    opt.append(best_st)
    previous = best_st
 
    # Traceback to find optimal probabilities for all states - looking at "prev" to determine optimal pathway
    for t in range(len(V) - 2, -1, -1):
        opt.insert(0, V[t + 1][previous]["prev"])
        previous = V[t + 1][previous]["prev"]
 
    print ("The steps are " + " ".join(opt) + " with the highest probability being %s" % max_prob)
    
def dptable(V):
    yield " ".join(("%8d" % i) for i in range(len(V)))
    for state in V[0]:
        yield "%.7s: " % state + " ".join("%.12s" % ("%f" % v[state]["prob"]) for v in V)
