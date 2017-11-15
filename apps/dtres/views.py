from django.shortcuts import render
import json
# Create your views here.

def dtres(request):
	porcentaje = [5, 15, 20, 15, 30, 14, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	creditos = ['0', '1-16', '17-32', '33-48', '49-64', '65-80', '81-96',
				'97-112', '113-128', '129-144', '145-160', '161-176', '177-192',
				'193-208', '209-224', '225-240', '240+']
	data2 = []
	for i in range(17):
		dictdata = {'porcentaje': porcentaje[i],
					'creditos': creditos[i]}

		print(dictdata)
		print('hi')
		data2.append(dictdata)

	#data2 = [
    #  { "Word":"Hello", "Awesomeness":2000 },
    #  { "Word":"World", "Awesomeness":3000 }
    #]
	print('hello')
	print(data2)
	data2 = json.dumps(data2)

	return render(request, "instantanea.html", {'data2':data2})

