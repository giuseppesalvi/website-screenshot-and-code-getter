from htmldom import htmldom
#import pprint
import sys

def print_recursively(node, depth):
    if(len(node)>0 and depth < 3):
        for n in node:
             print_recursively(n, depth + 1)
    print(node)

if __name__ == "__main__":

    args = sys.argv
    website = args[1] 
    domain = website.split("//www.")[-1].split("/")[0]
    dom = htmldom.HtmlDom(website)
    dom = dom.createDom()
    
    # Find all the links present on a page and prints its "href" value
    #a = dom.find( "a" )
    #for link in a:
    #    print( link.attr( "href" ) )
    
    # Find all elements and print it: problem, they are still objects
    # all = dom.find("*")
    #for element in all:
    #    print(element)
    
    # Print the python object as a dict, problem: internal values are still objects
    #print(dom.__dict__)
    
    # Try to print the dom with pretty print
    #pprint.pprint(dom)
    
    # Try to print recursively: problem recursion depth limit
    #print_recursively(dom.__dict__, 0)

    # Kinda works
    #a = dom.find("a")
    #print(a.html()) 

    #all = dom.find("*")
    #for node in all:
    	#print(node.html())

    with open("results/" + domain + ".html", "w") as f:
        all = dom.find("*")
        for node in all:
    	    f.write(node.html())
	
   

