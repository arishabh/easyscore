from pandas import read_csv
data = {}

def rate(tot, cgpa, sgpa, dist):
    mul = 10
    coef = 96/11.0

    rating = 0
    gpa_diff = cgpa-sgpa
    gpa_off = mul*gpa_diff

    rating = (100*dist[0]/tot) + gpa_off
    print(rating)
    print(dist)
    for i in range(12):
        rating += ((96-(i*coef))*dist[i+1]/tot)
    return rating

if __name__=='__main__':
    for i in range(9):
        info = read_csv('info/raw_data/'+str(i+1)+'.csv', low_memory=False, header=0).values
        for d in info:
            term = d[0].split()[0]
            if(term == 'TERM'): continue
            if(not(term == 'Fall' or term == 'Spring')): continue
            if(d[12] == 'NR'): continue
            c = d[5]+str(d[6])
            prof = d[9]
            r = rate(int(d[11]), float(d[13]), float(d[14]), list(map(int, d[20:33])))
            if c not in data:
                data[c] = {term:{prof: [r, 1]}}
            else:
                if term in data[c]:
                    if prof in data[c][term]:
                        data[c][term][prof] = [((data[c][term][prof][0]*data[c][term][prof][1])+r)/(data[c][term][prof][1]+1), data[c][term][prof][1] + 1]
                    else:
                        data[c][term][prof] = [r, 1]
                else:
                    data[c][term] = {prof: [r, 1]}
    rem=[]
    for d in data:
        if len(data[d]) <= 1:
            rem.append(d)
    for a in rem:
        del data[a]

    fall = []
    spring = []
    for d in data:
        a = data[d]['Fall']
        v = data[d]['Spring']
        for p in a:
            if p in v:
                fall.append(data[d]['Fall'][p][0])
        # for p in v:
                spring.append(data[d]['Spring'][p][0])

    print(len(fall))
    fall_avg = sum(fall)/len(fall)
    print("Fall Average EasyScore: " + str(fall_avg))
    spring_avg = sum(spring)/len(spring)
    print(len(spring))
    print("Spring Average Easyscore: " + str(spring_avg))
    # print(data)
