import numpy.random as rnd

V = 7
pn1 = 0.186
pn2 = 0.433
pm1 = 0.375
g1 = 0.26
g2 = 0.25


def gen_N_lifetime(state):
    par = g1 * state[0] + 2 * g1 * state[1] + 0.1
    return rnd.exponential(1/par)

def gen_M_lifetime(state):
    par = 3 * g2 * state[0] + g2 * state[1]
    return rnd.exponential(1/par)

def simulate():
    states = []
    objects = []
    t = 0
    obj_number = 1
    system = [{"Id": obj_number,
               "Type": "N",
               "Birth": t,
               "Death": t + gen_N_lifetime((0, 0)),
               "Child1": -1,
               "Child2": -1}]
    
    print("####    TABLE 1    ####")
    print(1, t, "SN(1)", system[0].get("Death"), -1, end = " ")

    for event_number in range(2, 101):
        system.sort(key = lambda i: i.get("Death"))
        N = len([i for i in system if i.get("Type") == "N"])
        M = len([i for i in system if i.get("Type") == "M"])
        states.append((N, M))
        curr_obj = system[0]
        print(N, M, curr_obj.get("Death") - t, curr_obj.get("Id"), curr_obj.get("Type"))
        system = system[1:]
        t = curr_obj.get("Death")
        temp = rnd.random()
        print(event_number, t, end=" ")
        if curr_obj.get("Type") == "N":
            if temp < pn1:
                dt = gen_N_lifetime((N, M))
                print("SN(1)", dt, -1, end = " ")
                obj_number += 1
                curr_obj["Child1"] = obj_number
                objects.append(curr_obj)
                system.append({"Id": obj_number,
                               "Type": "N",
                               "Birth": t,
                               "Death": t + dt,
                               "Child1": -1,
                               "Child2": -1})
            elif temp < pn1 + pn2:
                dt1 = gen_N_lifetime((N, M))
                dt2 = gen_N_lifetime((N, M))
                print("SN(2)", min(dt1, dt2), max(dt1, dt2), end = " ")
                obj_number += 1
                curr_obj["Child1"] = obj_number
                system.append({"Id": obj_number,
                               "Type": "N",
                               "Birth": t,
                               "Death": t + min(dt1, dt2),
                               "Child1": -1,
                               "Child2": -1})
                obj_number += 1
                curr_obj["Child2"] = obj_number
                system.append({"Id": obj_number,
                               "Type": "N",
                               "Birth": t,
                               "Death": t + max(dt1, dt2),
                               "Child1": -1,
                               "Child2": -1})
                objects.append(curr_obj)
            else:
                dtn = gen_N_lifetime((N, M))
                dtm = gen_M_lifetime((N, M))
                print("SN(3)", min(dtn, dtm), max(dtn, dtm), end = " ")
                obj_number += 1
                curr_obj["Child1"] = obj_number
                system.append({"Id": obj_number,
                               "Type": "N" if dtn <= dtm else "M",
                               "Birth": t,
                               "Death": t + min(dtn, dtm),
                               "Child1": -1,
                               "Child2": -1})
                obj_number += 1
                curr_obj["Child2"] = obj_number
                system.append({"Id": obj_number,
                               "Type": "N" if dtn > dtm else "M",
                               "Birth": t,
                               "Death": t + max(dtn, dtm),
                               "Child1": -1,
                               "Child2": -1})
                objects.append(curr_obj)
        else:
            if temp < pm1:
                dt = gen_M_lifetime((N, M))
                print("SM(1)", dt, -1, end = " ")
                obj_number += 1
                curr_obj["Child1"] = obj_number
                objects.append(curr_obj)
                system.append({"Id": obj_number,
                               "Type": "M",
                               "Birth": t,
                               "Death": t + dt,
                               "Child1": -1,
                               "Child2": -1})
            else:
                print("SM(0)", -1, -1, end = " ")
                objects.append(curr_obj)
    system.sort(key = lambda i: i.get("Death"))
    N = len([i for i in system if i.get("Type") == "N"])
    M = len([i for i in system if i.get("Type") == "M"])
    states.append((N, M))
    curr_obj = system[0]
    print(N, M, curr_obj.get("Death") - t, curr_obj.get("Id"), curr_obj.get("Type"))

    for i in system: objects.append(i)
    objects.sort(key = lambda i: i.get("Id"))
    print("\n\n####    TABLE 2    ####")
    for i in objects:
        print(i.get("Id"), i.get("Type"), i.get("Birth"),
        i.get("Death") - i.get("Birth"), i.get("Death"),
        i.get("Child1"), i.get("Child2"))
    
    print("\n\n####    TABLE 3    ####")
    for i in sorted(set(states)): print(i[0], i[1])

simulate()
