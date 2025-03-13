using InterfaceDemo;

class ClassA : IShape
{
    private int myNumber;
    public int MyNumber
    {
        get
        {
            return myNumber;
        }
        set
        {
            if (value < 0)
            {
                myNumber = 0;
            }
            else
            {
                myNumber = value;
            }
        }
    }

    public void InterfaceMethod()
    {
        Console.WriteLine("The number is {0}", myNumber);
    }
}

class Program
{
    static void Main(string[] args)
    {
        ClassA a = new ClassA();
        a.MyNumber = 5;
        a.InterfaceMethod();
    }
}