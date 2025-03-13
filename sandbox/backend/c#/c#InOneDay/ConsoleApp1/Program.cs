string userName;
int userBornYear;
int currentYear = DateTime.Now.Year;

Console.WriteLine("What is your name?");
userName = Console.ReadLine() ?? string.Empty;
Console.Write("What year were you born?");
userBornYear = Convert.ToInt32(Console.ReadLine());

Console.WriteLine("Hello World! My name is {0}. I was born in {1} so I am {2} years old", userName, userBornYear, currentYear - userBornYear);