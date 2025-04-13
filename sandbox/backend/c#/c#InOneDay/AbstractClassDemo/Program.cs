using AbstractClassDemo;

class ClassA : MyAbstractClass
{
    public override void PrintMessageAbstract()
    {
        System.Console.WriteLine("Hello from ClassA");
    }
}

class Program
{
    static void Main(string[] args)
    {
        //MyAbstractClass abClass = new MyAbstractClass();
        ClassA a = new ClassA();
        a.PrintMessage();
        a.PrintMessageAbstract();
        Console.Read();
    }
}
