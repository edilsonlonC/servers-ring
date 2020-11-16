#!/bin/bash

args=("$@")
first_server=0
rm -r [0-9]*
for i in ${args[@]}
do
	if [ $i == 5555 ];
	then 
		echo 'here'
		gnome-terminal -e "zsh -c 'python server.py -p $i -a localhost;zsh;'"
		$first_server = $i
	else
		echo $first_server
		gnome-terminal -e "zsh -c 'python server.py -p $i -sc localhost:5555 -a localhost;zsh;'"
	fi	
done

echo ${args[@]}
