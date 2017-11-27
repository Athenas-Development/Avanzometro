def granularizador(g):
	if g >= 121:
		g = 240

	if 240%g != 0:
		g = int(240/(240//g))

	if g <= 0:
		return False

	categorias = (240//g)
	creditos = []

	inicio = 1

	if g != 1:
		for i in range(1,categorias+1):
			final = ((240//categorias) * i)
			if inicio != final:
				creditos.append(str(inicio) + '-' + str(final))
			else:
				creditos.append(str(inicio))
			inicio = ((240//categorias) * i) + 1

		if final != 240:
			creditos.append(str(final) + '-' + str(240))

	else:
		for i in range(240):
			creditos.append(str(i+1))

	creditos = ['0'] + creditos + ['240+']

	return creditos