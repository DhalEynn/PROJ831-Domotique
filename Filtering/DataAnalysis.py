#def temporalFrequence(category, id):
	#list_
def link(category, id, time):
	list_actions = #requete sql tout les action fait par l'item category + id
	dico_frequency = {}
    nb_actions = len(list_actions)
	for action in list_actions:
		previous_action = #requete sql tout les action réalisé time avant action par un autre élément
		for p_action in previous_action:
			category_action = 
			id_action = 
			comande_action =
			if ( dico_frequency.get(category_action, {}).get(id_action, {}).get(comande_action) ):
				dico_frequency[category_action][id_action][comande_action] += 1
			else:
				dico_frequency[category_action] = {id_action: {comande_action 1}}
                
        ax = df['name'].value_counts().plot(kind='bar',figsize=(14,8),title="Number for each Owner Name")                           
        ax.set_xlabel("Owner Names")
        ax.set_ylabel("Frequency")
        return(dico_frequency , nb_actions)
   
def graph(dict_frequency, nb_actions):
    list_object=[]
    list_objet_frequency = []
    for key_category in dict_frequency.keys():
        for key_id in dict_frequency[key_category].keys():
            nb = 0
            for key_comande in dict_frequency[key_category][key_id].keys():
                nb += dict_frequency[key_category][key_id][key_comande]
            list_object += [key_category + key_id]
            list_objet_frequency += [nb/nb_actions]
    fig = go.Figure([go.Bar(x=list_object, y=list_objet_frequency)])
    plot(fig)
                 
