# This is just some junk code that may be needed at a later time
#

 # Adding different buttons depending on how many people have already
    # selected their products

    # Adding next button functionality
    def nextPressed():
        # Closing window to move to next person
        root.destroy()

    # If first person, only add next button
    if x == 0:
        # Creating new frame to keep button
        frame = Frame(root)
        frame.pack()
        
        # Creating button
        nextButton = tkinter.Button( frame, text = "Next person",
                                     command = nextPressed)
        nextButton.pack()

    # If people in the middle, add next and previous buttons
    else:
        if x < (int(number_of_people) - 1):
            # Creating new frame to keep buttons
            frame = Frame(root)
            frame.pack()

            # Creating previous button
            previousButton = tkinter.Button(frame, text = "Previous person")
            previousButton.pack( side = LEFT)

            # Creating next button
            nextButton = tkinter.Button( frame, text = "Next person",
                                         command = nextPressed)
            nextButton.pack( side = RIGHT)

        # If last person, add previous person and finalize buttons
        else:
            # Creating new frame to keep buttons
            frame = Frame(root)
            frame.pack()

            # Creating preivous button
            previousButton = tkinter.Button(frame, text = "Previous person")
            previousButton.pack( side = LEFT)

            # Creating finalize button
            endButton = tkinter.Button( frame, text = "Finalize")
            endButton.pack( side = RIGHT)
      
