"""
This file is set to run from the command line and set parameters
"""
import sys


from password_model.predict import filter_password

import argparse
from base_func.analyse_result import analyse_result

from hit_git_tf import *
from filter.filter_pattern_word import filter_pattern_word, filter_pattern_word_single
from filter.filter_similarstr import combine_similarstr

global log_path

import pyfiglet



if __name__ == '__main__':
	banner = pyfiglet.figlet_format("SecretDetection")
	banner2 = """                                               
	------------------- by @Kellanz -------------------
	"""
	print(banner)
	print(banner2)
	parser = argparse.ArgumentParser(description='Parameter Description')



	parser.add_argument('--path', dest='path', type=str, help='Enter the root path of the file to be tested', default="./test")
	parser.add_argument('--mode', dest='mode', type=str, help='Scan mode, divided into: scan and, entropy', default="scan")
	parser.add_argument('--entropy_path', dest='entropy_path', type=str, help='Entropy usage path', default="./data/entropy_result.bin")
	parser.add_argument('--regex', dest='regex', type=str, help='regex', default='./data/regex/regex_machine_human_v2.json')
	parser.add_argument('--save_name', dest='save_name', type=str, help='Save the file name for easy identification', default="all_result")
	parser.add_argument('--pre_loc', dest='pre_loc', type=str, help='Continue with previous testing loc——pre_test_root', default="None")
	parser.add_argument('--hit_dict', dest='hit_dict', type=str, help=' previous hit_dict', default="None")
	parser.add_argument('--size_limit', dest='size_limit', type=int, help=' size_limit of file', default=10 * 1024 * 1024)
	parser.add_argument('--core_num', dest='core_num', type=int, help=' nums of core', default=multiprocessing.cpu_count()-5)
	parser.add_argument('--timeout_seconds', dest='timeout_seconds', type=int, help='timeout_seconds',
						default=3000)
	if len(sys.argv) == 1:
		parser.print_help()
		sys.exit(1)
	args = parser.parse_args()
	print(f"scanned path:{args.path}")
	print(f"scan mode: {args.mode}")

	save_root = make_result()  # create folder to save res
	log_path = os.path.join(save_root, "log.json")
	logger_instance = setup_logger(log_path)
	logger_instance.info(f"--mode:{args.mode},--path:{args.path},--regex:{args.regex}, --entropy_path:{args.entropy_path}, --save_name:{args.save_name},--pre_loc{args.pre_loc},--size_limit{args.size_limit}")

	file_list=get_files(args.path,args.size_limit)

	print(f"file nums :{len(file_list)}")
	
	if args.mode == "scan":
		time1=time.time()
		manager = Manager()
		single_dict = manager.list()
		duplicate_dict=manager.list()
		shared_variable = manager.Value('i', 0)
		num_cores = int(args.core_num)

		pool = Pool(processes=num_cores)
		if (args.regex).endswith('.bin'):
			rules_single = read_dict_bin(args.regex)
		elif (args.regex).endswith('.json'):
			rules_single = read_json(args.regex)	
		batch_size=len(file_list)//num_cores
		with Pool(processes=num_cores) as pool:
			for i in range(num_cores):
				start_idx = i * batch_size
				end_idx = (i + 1) * batch_size if i < num_cores - 1 else len(file_list)
				batch_files = file_list[start_idx:end_idx]
				pool.apply_async(scan_filelist_tf, (rules_single,batch_files, single_dict,duplicate_dict,shared_variable,log_path,args.timeout_seconds))
			pool.close()
			pool.join()
		result_single_dict = list(single_dict)
		result_duplicate_dict=list(duplicate_dict)
		hit_dict = result_single_dict

		print(f"length_single_dict:{len(single_dict)}")
		print(f"length_result_duplicate_dict:{len(result_duplicate_dict)}")

		save_dict2bin(hit_dict,"hit_dict",save_root)
		save_dict2bin(result_duplicate_dict,"result_duplicate_dict",save_root)        #save res

		current_path = os.path.dirname(os.path.abspath(__file__))
		target_path = os.path.abspath(os.path.join(current_path, './data/fixed_top_english_words_mixed_500000.json'))
		words_list=read_json(target_path)
		patterns = []
		target_path = os.path.abspath(os.path.join(current_path, './data/patterns.txt'))
		with open(target_path, "r") as f:
			patterns = f.readlines()
		patterns = [pattern.strip() for pattern in patterns]
		batch_size=len(hit_dict)//num_cores
		tmp_filter=[]
		filtered=[]
		with Pool(processes=num_cores) as pool:
			for i in range(num_cores):
				start_idx = i * batch_size
				end_idx = (i + 1) * batch_size if i < num_cores - 1 else len(hit_dict)
				batch_files = hit_dict[start_idx:end_idx]
				tmp_filter.append(pool.apply_async(filter_pattern_word, (batch_files,words_list,patterns,rules_single,log_path)))
			pool.close()
			pool.join()
		for tmp in tmp_filter:
			tmp=tmp.get()
			filtered.extend(tmp)

		print(f"hit:{len(filtered)}")
		save_dict2bin(filtered,"origin_filtered",save_root)        #save res

		pass_dict=[]
		token_dict=[]
		for tmp in filtered:
			if 'pass' in tmp['rule_name']:
				pass_dict.append(tmp)
			else:
				token_dict.append(tmp)
		tmp_pass_filter=[]
		batch_size=len(pass_dict)//num_cores
		with Pool(processes=num_cores) as pool:
			for i in range(num_cores):
				start_idx = i * batch_size
				end_idx = (i + 1) * batch_size if i < num_cores - 1 else len(pass_dict)
				batch_files = pass_dict[start_idx:end_idx]
				tmp_pass_filter.append(pool.apply_async(filter_password, ([batch_files])))
			pool.close()
			pool.join()
		result=token_dict
		for tmp in tmp_pass_filter:
			tmp=tmp.get()
			result.extend(tmp)

		result=combine_similarstr(result)
		#——————————————
		save_hit_dict_trufflehog(result,args.save_name,save_root)  #save res

		logger_instance.info(f"time_wasted:{time.time()-time1}")
		analyse_result(result)

	elif args.mode == "entropy":
		pass
