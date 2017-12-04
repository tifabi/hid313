output: main.o
	g++ main.o -o output

main.o: stock.py
	g++ -c stock.py

clean:
	rm *.o output