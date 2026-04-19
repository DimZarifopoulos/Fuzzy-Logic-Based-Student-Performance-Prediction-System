import numpy as np
import matplotlib.pyplot as plt

# Ορισμός μιας τριγωνικής συνάρτησης συμμετοχής
def trimf(x, params):
    a, b, c = params
    x = np.array(x, dtype=float)
    return np.maximum(np.minimum((x - a) / (b - a + 1e-9), (c - x) / (c - b + 1e-9)), 0.0)

# Ορισμός μιας τραπεζοειδούς συνάρτησης συμμετοχής
def trapmf(x, params):
    x = np.array(x)
    a, b, c, d = params
    return np.where(x <= a, 0,
        np.where(x <= b, (x - a) / (b - a),
            np.where(x <= c, 1,
                np.where(x <= d, (d - x) / (d - c), 0))))

# οπτικοποίηση των συναρτήσεων συμμετοχής χρησιμοποιώντας τη Matplotlib
def plot_membership(x, y, labels, title):
    plt.figure(figsize=(6,4))
    for i in range(len(y)):
        plt.plot(x, y[i], label=labels[i])
    plt.title(title)
    plt.xlabel("Value")
    plt.ylabel("Membership")
    plt.legend()
    plt.grid(True)
    plt.show()

# ορισμός του γενικού περιβάλλοντος των γραφημάτων
P = np.arange(0, 101, 1)   # Συμμετοχή 0-100%
A = np.arange(0, 101, 1)   # Βαθμός εργασίας 0-100
E = np.arange(0, 101, 1)   # Βαθμός εξέτασης 0-100
Abs = np.arange(0, 31, 1)  # Απουσίες 0-30 days
Perf = np.arange(0, 101, 1) # Απόδοση 0-100

# ορισμός των ασαφών συνόλων
P_low = trimf(P, [0, 25, 50])
P_med = trimf(P, [25, 50, 75])
P_high = trimf(P, [50, 100, 100])

A_poor = trimf(A, [0, 25, 50])
A_avg  = trimf(A, [40, 60, 80])
A_good = trimf(A, [60, 100, 100])

E_poor = trimf(E, [0, 25, 50])
E_avg  = trimf(E, [40, 60, 80])
E_good = trimf(E, [60, 100, 100])

Abs_many = trimf(Abs, [10, 20, 30])
Abs_few  = trimf(Abs, [0, 5, 15])

Perf_low = trimf(Perf, [0, 25, 50])
Perf_med = trimf(Perf, [30, 50, 70])
Perf_high= trimf(Perf, [50, 100, 100])

# γραφική αναπαράσταση των ασαφών συνόλων
plot_membership(P, [P_low, P_med, P_high], ["Low", "Medium", "High"], "Participation")
plot_membership(A, [A_poor, A_avg, A_good], ["Poor", "Average", "Good"], "Assignments")
plot_membership(E, [E_poor, E_avg, E_good], ["Poor", "Average", "Good"], "Exams")
plot_membership(Abs, [Abs_few, Abs_many], ["Few", "Many"], "Absences")
plot_membership(Perf, [Perf_low, Perf_med, Perf_high], ["Low", "Medium", "High"], "Performance (Output)")

# Κανόνες
rules = [
    # Χαμήλη συμμετοχή
    (lambda f: min(f['P_low'], f['A_poor'], f['E_poor'], f['Abs_few']), 'Low',
     "IF Participation=Low AND Assignments=Poor AND Exams=Poor AND Absences=Few THEN Performance=Low"),
    (lambda f: min(f['P_low'], f['A_poor'], f['E_poor'], f['Abs_many']), 'Low',
     "IF Participation=Low AND Assignments=Poor AND Exams=Poor AND Absences=Many THEN Performance=Low"),
    (lambda f: min(f['P_low'], f['A_poor'], f['E_avg'], f['Abs_few']), 'Low',
     "IF Participation=Low AND Assignments=Poor AND Exams=Average AND Absences=Few THEN Performance=Low"),
    (lambda f: min(f['P_low'], f['A_poor'], f['E_avg'], f['Abs_many']), 'Low',
     "IF Participation=Low AND Assignments=Poor AND Exams=Average AND Absences=Many THEN Performance=Low"),
    (lambda f: min(f['P_low'], f['A_poor'], f['E_good'], f['Abs_few']), 'Medium',
     "IF Participation=Low AND Assignments=Poor AND Exams=Good AND Absences=Few THEN Performance=Medium"),
    (lambda f: min(f['P_low'], f['A_poor'], f['E_good'], f['Abs_many']), 'Medium',
     "IF Participation=Low AND Assignments=Poor AND Exams=Good AND Absences=Many THEN Performance=Medium"),

    (lambda f: min(f['P_low'], f['A_avg'], f['E_poor'], f['Abs_few']), 'Low',
     "IF Participation=Low AND Assignments=Average AND Exams=Poor AND Absences=Few THEN Performance=Low"),
    (lambda f: min(f['P_low'], f['A_avg'], f['E_poor'], f['Abs_many']), 'Low',
     "IF Participation=Low AND Assignments=Average AND Exams=Poor AND Absences=Many THEN Performance=Low"),
    (lambda f: min(f['P_low'], f['A_avg'], f['E_avg'], f['Abs_few']), 'Medium',
     "IF Participation=Low AND Assignments=Average AND Exams=Average AND Absences=Few THEN Performance=Medium"),
    (lambda f: min(f['P_low'], f['A_avg'], f['E_avg'], f['Abs_many']), 'Low',
     "IF Participation=Low AND Assignments=Average AND Exams=Average AND Absences=Many THEN Performance=Low"),
    (lambda f: min(f['P_low'], f['A_avg'], f['E_good'], f['Abs_few']), 'Medium',
     "IF Participation=Low AND Assignments=Average AND Exams=Good AND Absences=Few THEN Performance=Medium"),
    (lambda f: min(f['P_low'], f['A_avg'], f['E_good'], f['Abs_many']), 'Medium',
     "IF Participation=Low AND Assignments=Average AND Exams=Good AND Absences=Many THEN Performance=Medium"),

    (lambda f: min(f['P_low'], f['A_good'], f['E_poor'], f['Abs_few']), 'Low',
     "IF Participation=Low AND Assignments=Good AND Exams=Poor AND Absences=Few THEN Performance=Low"),
    (lambda f: min(f['P_low'], f['A_good'], f['E_poor'], f['Abs_many']), 'Low',
     "IF Participation=Low AND Assignments=Good AND Exams=Poor AND Absences=Many THEN Performance=Low"),
    (lambda f: min(f['P_low'], f['A_good'], f['E_avg'], f['Abs_few']), 'Medium',
     "IF Participation=Low AND Assignments=Good AND Exams=Average AND Absences=Few THEN Performance=Medium"),
    (lambda f: min(f['P_low'], f['A_good'], f['E_avg'], f['Abs_many']), 'Medium',
     "IF Participation=Low AND Assignments=Good AND Exams=Average AND Absences=Many THEN Performance=Medium"),
    (lambda f: min(f['P_low'], f['A_good'], f['E_good'], f['Abs_few']), 'High',
     "IF Participation=Low AND Assignments=Good AND Exams=Good AND Absences=Few THEN Performance=High"),
    (lambda f: min(f['P_low'], f['A_good'], f['E_good'], f['Abs_many']), 'Low',
     "IF Participation=Low AND Assignments=Good AND Exams=Good AND Absences=Many THEN Performance=Low"),

    # Μέτρια συμμετοχή
    (lambda f: min(f['P_med'], f['A_poor'], f['E_poor'], f['Abs_few']), 'Low',
     "IF Participation=Medium AND Assignments=Poor AND Exams=Poor AND Absences=Few THEN Performance=Low"),
    (lambda f: min(f['P_med'], f['A_poor'], f['E_poor'], f['Abs_many']), 'Low',
     "IF Participation=Medium AND Assignments=Poor AND Exams=Poor AND Absences=Many THEN Performance=Low"),
    (lambda f: min(f['P_med'], f['A_poor'], f['E_avg'], f['Abs_few']), 'Low',
     "IF Participation=Medium AND Assignments=Poor AND Exams=Average AND Absences=Few THEN Performance=Low"),
    (lambda f: min(f['P_med'], f['A_poor'], f['E_avg'], f['Abs_many']), 'Low',
     "IF Participation=Medium AND Assignments=Poor AND Exams=Average AND Absences=Many THEN Performance=Low"),
    (lambda f: min(f['P_med'], f['A_poor'], f['E_good'], f['Abs_few']), 'Medium',
     "IF Participation=Medium AND Assignments=Poor AND Exams=Good AND Absences=Few THEN Performance=Medium"),
    (lambda f: min(f['P_med'], f['A_poor'], f['E_good'], f['Abs_many']), 'Medium',
     "IF Participation=Medium AND Assignments=Poor AND Exams=Good AND Absences=Many THEN Performance=Medium"),

    (lambda f: min(f['P_med'], f['A_avg'], f['E_poor'], f['Abs_few']), 'Low',
     "IF Participation=Medium AND Assignments=Average AND Exams=Poor AND Absences=Few THEN Performance=Low"),
    (lambda f: min(f['P_med'], f['A_avg'], f['E_poor'], f['Abs_many']), 'Low',
     "IF Participation=Medium AND Assignments=Average AND Exams=Poor AND Absences=Many THEN Performance=Low"),
    (lambda f: min(f['P_med'], f['A_avg'], f['E_avg'], f['Abs_few']), 'Medium',
     "IF Participation=Medium AND Assignments=Average AND Exams=Average AND Absences=Few THEN Performance=Medium"),
    (lambda f: min(f['P_med'], f['A_avg'], f['E_avg'], f['Abs_many']), 'Medium',
     "IF Participation=Medium AND Assignments=Average AND Exams=Average AND Absences=Many THEN Performance=Medium"),
    (lambda f: min(f['P_med'], f['A_avg'], f['E_good'], f['Abs_few']), 'High',
     "IF Participation=Medium AND Assignments=Average AND Exams=Good AND Absences=Few THEN Performance=High"),
    (lambda f: min(f['P_med'], f['A_avg'], f['E_good'], f['Abs_many']), 'Medium',
     "IF Participation=Medium AND Assignments=Average AND Exams=Good AND Absences=Many THEN Performance=Medium"),

    (lambda f: min(f['P_med'], f['A_good'], f['E_poor'], f['Abs_few']), 'Low',
     "IF Participation=Medium AND Assignments=Good AND Exams=Poor AND Absences=Few THEN Performance=Low"),
    (lambda f: min(f['P_med'], f['A_good'], f['E_poor'], f['Abs_many']), 'Low',
     "IF Participation=Medium AND Assignments=Good AND Exams=Poor AND Absences=Many THEN Performance=Low"),
    (lambda f: min(f['P_med'], f['A_good'], f['E_avg'], f['Abs_few']), 'High',
     "IF Participation=Medium AND Assignments=Good AND Exams=Average AND Absences=Few THEN Performance=High"),
    (lambda f: min(f['P_med'], f['A_good'], f['E_avg'], f['Abs_many']), 'Medium',
     "IF Participation=Medium AND Assignments=Good AND Exams=Average AND Absences=Many THEN Performance=Medium"),
    (lambda f: min(f['P_med'], f['A_good'], f['E_good'], f['Abs_few']), 'High',
     "IF Participation=Medium AND Assignments=Good AND Exams=Good AND Absences=Few THEN Performance=High"),
    (lambda f: min(f['P_med'], f['A_good'], f['E_good'], f['Abs_many']), 'High',
     "IF Participation=Medium AND Assignments=Good AND Exams=Good AND Absences=Many THEN Performance=High"),

    # Υψηλή συμμετοχή
    (lambda f: min(f['P_high'], f['A_poor'], f['E_poor'], f['Abs_few']), 'Low',
     "IF Participation=High AND Assignments=Poor AND Exams=Poor AND Absences=Few THEN Performance=Low"),
    (lambda f: min(f['P_high'], f['A_poor'], f['E_poor'], f['Abs_many']), 'Low',
     "IF Participation=High AND Assignments=Poor AND Exams=Poor AND Absences=Many THEN Performance=Low"),
    (lambda f: min(f['P_high'], f['A_poor'], f['E_avg'], f['Abs_few']), 'Low',
     "IF Participation=High AND Assignments=Poor AND Exams=Average AND Absences=Few THEN Performance=Low"),
    (lambda f: min(f['P_high'], f['A_poor'], f['E_avg'], f['Abs_many']), 'Low',
     "IF Participation=High AND Assignments=Poor AND Exams=Average AND Absences=Many THEN Performance=Low"),
    (lambda f: min(f['P_high'], f['A_poor'], f['E_good'], f['Abs_few']), 'Medium',
     "IF Participation=High AND Assignments=Poor AND Exams=Good AND Absences=Few THEN Performance=Medium"),
    (lambda f: min(f['P_high'], f['A_poor'], f['E_good'], f['Abs_many']), 'Medium',
     "IF Participation=High AND Assignments=Poor AND Exams=Good AND Absences=Many THEN Performance=Medium"),

    (lambda f: min(f['P_high'], f['A_avg'], f['E_poor'], f['Abs_few']), 'Low',
     "IF Participation=High AND Assignments=Average AND Exams=Poor AND Absences=Few THEN Performance=Low"),
    (lambda f: min(f['P_high'], f['A_avg'], f['E_poor'], f['Abs_many']), 'Low',
     "IF Participation=High AND Assignments=Average AND Exams=Poor AND Absences=Many THEN Performance=Low"),
    (lambda f: min(f['P_high'], f['A_avg'], f['E_avg'], f['Abs_few']), 'Medium',
     "IF Participation=High AND Assignments=Average AND Exams=Average AND Absences=Few THEN Performance=Medium"),
    (lambda f: min(f['P_high'], f['A_avg'], f['E_avg'], f['Abs_many']), 'Medium',
     "IF Participation=High AND Assignments=Average AND Exams=Average AND Absences=Many THEN Performance=Medium"),
    (lambda f: min(f['P_high'], f['A_avg'], f['E_good'], f['Abs_few']), 'High',
     "IF Participation=High AND Assignments=Average AND Exams=Good AND Absences=Few THEN Performance=High"),
    (lambda f: min(f['P_high'], f['A_avg'], f['E_good'], f['Abs_many']), 'High',
     "IF Participation=High AND Assignments=Average AND Exams=Good AND Absences=Many THEN Performance=High"),

    (lambda f: min(f['P_high'], f['A_good'], f['E_poor'], f['Abs_few']), 'Medium',
     "IF Participation=High AND Assignments=Good AND Exams=Poor AND Absences=Few THEN Performance=Medium"),
    (lambda f: min(f['P_high'], f['A_good'], f['E_poor'], f['Abs_many']), 'Medium',
     "IF Participation=High AND Assignments=Good AND Exams=Poor AND Absences=Many THEN Performance=Medium"),
    (lambda f: min(f['P_high'], f['A_good'], f['E_avg'], f['Abs_few']), 'High',
     "IF Participation=High AND Assignments=Good AND Exams=Average AND Absences=Few THEN Performance=High"),
    (lambda f: min(f['P_high'], f['A_good'], f['E_avg'], f['Abs_many']), 'Medium',
     "IF Participation=High AND Assignments=Good AND Exams=Average AND Absences=Many THEN Performance=Medium"),
    (lambda f: min(f['P_high'], f['A_good'], f['E_good'], f['Abs_few']), 'High',
     "IF Participation=High AND Assignments=Good AND Exams=Good AND Absences=Few THEN Performance=High"),
    (lambda f: min(f['P_high'], f['A_good'], f['E_good'], f['Abs_many']), 'High',
     "IF Participation=High AND Assignments=Good AND Exams=Good AND Absences=Many THEN Performance=High"),
]

# Ασαφοποίηση της εισόδου
def fuzzy_inference(p_value, a_value, e_value, abs_value):

    # Υπολογισμός membership values για συγκεκριμένες εισόδους
    f = {
        'P_low':  trimf([p_value], [0, 25, 50])[0],
        'P_med':  trimf([p_value], [25, 50, 75])[0],
        'P_high': trimf([p_value], [50, 100, 100])[0],

        'A_poor': trimf([a_value], [0, 25, 50])[0],
        'A_avg':  trimf([a_value], [40, 60, 80])[0],
        'A_good': trimf([a_value], [60, 100, 100])[0],

        'E_poor': trimf([e_value], [0, 25, 50])[0],
        'E_avg':  trimf([e_value], [40, 60, 80])[0],
        'E_good': trimf([e_value], [60, 100, 100])[0],

        'Abs_few':  trimf([abs_value], [0, 5, 15])[0],
        'Abs_many': trimf([abs_value], [10, 20, 30])[0],
    }

    # Αρχικοποίηση aggregated output
    agg_low = np.zeros_like(Perf, dtype=float)
    agg_med = np.zeros_like(Perf, dtype=float)
    agg_high = np.zeros_like(Perf, dtype=float)

    rules_applied = []  # λίστα για να αποθηκεύουμε ποιοί κανόνες ενεργοποιούνται

    # Εκτέλεση κανόνων
    for i, (rule, outcome, description) in enumerate(rules, start=1):
        activation = rule(f)
        if activation > 0:
            rules_applied.append((i, outcome, activation, description))
            if outcome == 'Low':
                agg_low = np.maximum(agg_low, np.minimum(activation, Perf_low))
            elif outcome == 'Medium':
                agg_med = np.maximum(agg_med, np.minimum(activation, Perf_med))
            elif outcome == 'High':
                agg_high = np.maximum(agg_high, np.minimum(activation, Perf_high))

    # Ένωση των outputs
    aggregated = np.maximum(agg_low, np.maximum(agg_med, agg_high))

    # Ασαφοποίηση χρησιμοποιώντας Centroid
    if np.sum(aggregated) == 0:
        crisp_value = 0
    else:
        crisp_value = np.sum(Perf * aggregated) / np.sum(aggregated)

    # Εκτυπώσεις
    print(f"\nInput values: Participation={p_value}, Assignment grade={a_value}, Exam grade={e_value}, Absences={abs_value}")

    # εμφάνιση των υπολογισόμενων τιμών
    print(f">Fuzzified values for Participation={p_value}:")
    print(f" Low: {f['P_low']:.2f}")
    print(f" Medium: {f['P_med']:.2f}")
    print(f" High: {f['P_high']:.2f}")

    print(f">Fuzzified values for Assignment grade={a_value}:")
    print(f" Poor: {f['A_poor']:.2f}")
    print(f" Average: {f['A_avg']:.2f}")
    print(f" Good: {f['A_good']:.2f}")

    print(f">Fuzzified values for Exam grade={e_value}:")
    print(f" Poor: {f['E_poor']:.2f}")
    print(f" Average: {f['E_avg']:.2f}")
    print(f" Good: {f['E_good']:.2f}")

    print(f">Fuzzified values for Absences={abs_value}:")
    print(f" Few: {f['Abs_few']:.2f}")
    print(f" Many: {f['Abs_many']:.2f}")

    print("Rules applied:")
    for idx, out, act, desc in rules_applied:
        print(f" - Rule {idx}: {desc} [activation={act:.2f}]")
    print(f"Final defuzzified performance: {crisp_value:.2f}\n")

    # Plot aggregated output
    plt.figure(figsize=(6, 4))
    plt.plot(Perf, Perf_low, '--', color='orange', label="Low")
    plt.plot(Perf, Perf_med, '--', color='green', label="Medium")
    plt.plot(Perf, Perf_high, '--', color='blue', label="High")
    plt.fill_between(Perf, aggregated, alpha=0.4, color="gray", label="Aggregated")
    plt.axvline(crisp_value, color='red', linestyle='--', label=f"Defuzzified={crisp_value:.2f}")
    plt.title("Aggregated Output & Defuzzified Result")
    plt.xlabel("Performance")
    plt.ylabel("Membership")
    plt.legend()
    plt.grid(True)
    plt.show()

    return crisp_value, f

value, memberships = fuzzy_inference(p_value=70, a_value=80, e_value=65, abs_value=5)
