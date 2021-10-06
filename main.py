#This is a psuedocode starter representation for a program called Pokemon Route Search


Main:
    Print explanation
    Application loop


Loop:
	Ask user which mode they would like to use
		Check if valid answer
		Set current game mode to answer
    	Ask user for pokemon/route
		Use an api wrapper to validate response from wikipedia
        retrieve data if valid
        Format data
	Print data in human readable format
	Ask if user would like to do another search, change search mode, or quit application
