namespace AbstractClassDemo;

abstract class MyAbstractClass
{
    private string message = "Hello C#!";

    public void PrintMessage()
    {
        System.Console.WriteLine(message);
    }

    public abstract void PrintMessageAbstract();

}
