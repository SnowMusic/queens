import csv

fname = 'hb_201705_callrecord.csv'

with open(fname,'rb') as csvfile:
	reader = csv.reader(csvfile)
	rows = [row[1] for row in reader]

a = 0
one = []

for obj in rows:
	if obj.strip():
		one.append(rows[a])
	a+=1


fname ='query_result.csv'

with open(fname,'rb') as csvfile:
	reader = csv.reader(csvfile)
	another = [row[1] for row in reader]

b = 0
two =[]

for obj1 in another:
	if obj1.strip():
		two.append(another[b])
	b+=1


print len(one)
print len(two)

dift = []

first = 0
needContinue =False

while first < len(one):
	second = 0
	while(second < len(two)):
		if one[first] == two[second]:
			needContinue = True
			break
		else : 
			needContinue = False

		second+=1

	if needContinue == False:
		dift.append(one[first])

	first+=1


first = 0
needContinue =False
third = one
one = two
two = third

while first < len(one):
	second = 0
	while(second < len(two)):
		if one[first] == two[second]:
			needContinue = True
			break
		else : 
			needContinue = False
			
		second+=1

	if needContinue == False:
		dift.append(one[first])

	first+=1

		
print dift





