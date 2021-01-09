#   class which implements operating on arrays as known in c++/c
#   usage:
#    from arrayLib import Array
#       array = Array(5,5)    -> definies array with size 5*5 equivalent of int array[5][5];
#   to modify values of array simply use:
#       array.modify(1,2,10)  -> where 1,2 stands for x,y and 10 stands for new value for array cell 
#   you can print this array with:
#       array.print()
#   you can also use:
#       array.print(1,2)      -> it increase width between array values in column and between rows

class Array:
    def __init__(self,height,width,placeholder=0):
        self.width=width
        self.height=height
        self.a=[[placeholder]*width]*height
        self.modify(0,0,placeholder)
        
    def modify(self,x,y,value):
        """Return modified array"""
        if(self.height < x or self.width < y):
            return False
        self.modifyRow = []
        self.modifyArray = []

        for i in range(self.width):
            if(i==y):
                self.modifyRow.append(value)
            else:
                self.modifyRow.append(self.a[x][i])

        for z in range(self.height):
            if(z==x):
                self.modifyArray.append(self.modifyRow)
            else:
                self.modifyArray.append(self.a[z])

        self.a = self.modifyArray
        return self.modifyArray

    def printArray(self,width_increase=0,height_increase=1):
        """Prints array with changed values. Changes from value given in f1 to t1 and f2 to t2. If neither f1 nor f2 is 0 it is changed to ' ' """ 
        if(width_increase<0):
            width_increase=0
        if(height_increase<1):
            height_increase=1
        for x in range(self.height):
            for y in range(self.width):
                
                print(self.modifyArray[x][y],end='')

                for w in range(width_increase):
                    print(' ',end='')

            for h in range(height_increase):
                print('')

    def printReplace(self,width_increase=0,height_increase=1,f1=1,t1='|',f2='',t2=''):
        if(width_increase<0):
            width_increase=0
        if(height_increase<1):
            height_increase=1
        for x in range(self.height):
            for y in range(self.width):
                if(self.modifyArray[x][y]==0 and f1 != 0 and f2!=0):
                    print(' ',end='')
                if(self.modifyArray[x][y]==f1):
                    print(t1,end='')
                if(self.modifyArray[x][y]==f2):
                    print(t2,end='')

                for w in range(width_increase):
                    print(' ',end='')
            for h in range(height_increase):
                print('')