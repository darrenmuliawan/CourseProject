import os,codecs,json

def main(dir_,out_file1,out_file2,dept_path,uni_path,names_path,url_path,loc_path,email_path,filter_file1,filter_file2):
	with open(uni_path,'r') as f:
		unis = f.readlines()

	with open(dept_path,'r') as f:
		depts = f.readlines()

	with open(names_path,'r') as f:
		names = f.readlines()

	with open(url_path,'r') as f:
		urls = f.readlines()

	with codecs.open(loc_path,'r',encoding='utf-8',errors='ignore') as f:
		locs = f.readlines()

	with codecs.open(email_path,'r',encoding='utf-8',errors='ignore') as f:
		emails = f.readlines()


	max_len = 15
	max_parts = 3
	non_names = ['curriculum','vitae','bio','professor','assistant',')','(','--','nat','center','sitemap','u.','2002','washington']

	corrected_names = []

	for name in names:
		parts = name.strip().split()
		corrected_name = ''
		for part in parts[:max_parts]:
			if len(part)<=max_len and part.lower() not in non_names and part.title() not in corrected_name.split():
				corrected_name += ' '+part.title()
		corrected_names.append(corrected_name)


	num_bios = len(os.listdir(dir_))-5

	print(emails[-2:],len(emails),len(corrected_names),len(locs),len(depts),len(unis),num_bios)

	with open(out_file1,'w') as f1:
		with codecs.open(out_file2,'w',encoding='utf-8',errors='ignore') as f2:
			for i in range(num_bios)[:-1]:
				f1.write('[None] '+str(i)+'.txt')
				f1.write('\n')
				if emails[i]=='\n':
					emails[i]='None'
				f2.write(str(i)+'.txt'+'\t'
					+unis[i].strip()+'\t'+depts[i].strip()+'\t'+corrected_names[i]+'\t'+urls[i].strip()+'\t'+locs[i].strip()+'\t'+emails[i].strip())
				f2.write('\n')

			f1.write('[None] '+str(num_bios-1)+'.txt')
			if emails[num_bios-1]=='\n':
					emails[num_bios-1]='None'
			f2.write(str(num_bios-1)+'.txt'+'\t'
				+unis[num_bios-1].strip()+'\t'+depts[num_bios-1].strip()+'\t'+corrected_names[num_bios-1]+'\t'+urls[num_bios-1].strip()+'\t'+locs[num_bios-1].strip()+'\t'+emails[num_bios-1].strip())

	unis_dict = {"unis":sorted([uni.strip() for uni in list(set(unis))])}
	all_countries = set()
	all_locs = set()

	for loc in locs:
		country = loc.split('\t')[1]
		all_countries.add(country.strip())
		all_locs.add(loc.replace('\t',', ').strip())

	all_countries = sorted(list(all_countries))
	all_locs = sorted(list(all_locs))
	all_locs = all_countries + all_locs

	locs_dict = {"locs":all_locs}

	json.dump(unis_dict,open(filter_file1,'w'))
	json.dump(locs_dict,open(filter_file2,'w'))

	

if __name__ == '__main__':
	main('../data/compiled_bios','../compiled_bios/dataset-full-corpus.txt','../data/compiled_bios/metadata.dat','../data/depts','../data/unis','../data/names.txt','../data/urls','../data/location','../data/emails','../data/filter_data/unis.json','../data/filter_data/locs.json')




