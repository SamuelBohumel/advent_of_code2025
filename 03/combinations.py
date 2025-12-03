class Combination :
    # Data array for combination
    Indices = None
    
    # Number of elements in the combination
    R = 0
    
    # The boolean array
    Flags = None
    
    # Starting index of the 1st tract of trues
    Start = 0
    
    # Ending index of the 1st tract of trues
    End = 0
    
    # Constructor
    def __init__(self, arr,  r) :
        self.Indices = arr
        self.R = r
        
    # Set the 1st r Booleans to true,
    # initialize Start and End
    def GetFirst(self) :
        self.Flags = [False] * (len(self.Indices))
        
        # Generate the very first combination
        i = 0
        while (i < self.R) :
            self.Flags[i] = True
            i += 1
            
        # Update the starting ending indices
        # of trues in the boolean array
        self.Start = 0
        self.End = self.R - 1
        self.Output()
        
    # Function that returns true if another
    # combination can still be generated
    def  HasNext(self) :
        return self.End < (len(self.Indices) - 1)
      
    # Function to generate the next combination
    def Next(self) :
      
        # Only one true in the tract
        if (self.Start == self.End) :
            self.Flags[self.End] = False
            self.Flags[self.End + 1] = True
            self.Start += 1
            self.End += 1
            while (self.End + 1 < len(self.Indices) and self.Flags[self.End + 1]) :
                self.End += 1
        else :
          
            # Move the End and reset the End
            if (self.Start == 0) :
                self.Flags[self.End] = False
                self.Flags[self.End + 1] = True
                self.End -= 1
            else :
                self.Flags[self.End + 1] = True
                
                # Set all the values to false starting from
                # index Start and ending at index End
                # in the boolean array
                i = self.Start
                while (i <= self.End) :
                    self.Flags[i] = False
                    i += 1
                    
                # Set the beginning elements to true
                i = 0
                while (i < self.End - self.Start) :
                    self.Flags[i] = True
                    i += 1
                    
                # Reset the End
                self.End = self.End - self.Start - 1
                self.Start = 0
        return self.Output()
        
    # Function to print the combination generated previouslt
    def Output(self) :
        i = 0
        count = 0
        result = []
        while (i < len(self.Indices) and count < self.R) :
          
            # If current index is set to true in the boolean array
            # then element at current index in the original array
            # is part of the combination generated previously
            if (self.Flags[i]) :
                result.append(self.Indices[i])
                # print(self.Indices[i], end ="")
                # print(" ", end ="")
                count += 1
            i += 1
        # print()
        return result