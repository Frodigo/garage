namespace FirstOOP
{
    class Staff
    {
        private string nameOfStaff;
        private const int hourlyRate = 30;
        private int hWorked;

        public Staff(string name)
        {
            nameOfStaff = name;
            Console.WriteLine("\n" + nameOfStaff);
            Console.WriteLine("----------------");
        }

        public Staff(string firstName, string lastName)
        {
            nameOfStaff = firstName + " " + lastName;
            Console.WriteLine("\n" + nameOfStaff);
            Console.WriteLine("----------------");
        }

        public int HoursWorked
        {
            get
            {
                return hWorked;
            }
            set
            {
                if (value > 0)
                    hWorked = value;
                else
                    hWorked = 0;
            }
        }

        // it can be also public int HoursWorked { get; private set; }

        public void PrintMessage()
        {
            Console.WriteLine("Calculating Pay...");
        }

        public int CalculatePay()
        {
            PrintMessage();
            int staffPay;
            staffPay = hWorked * hourlyRate;

            if (hWorked > 0)
                return staffPay;
            else
                return 0;
        }

        public int CalculatePay(int bonus, int allowance)
        {
            PrintMessage();
            if (hWorked > 0)
                return hWorked * hourlyRate + bonus + allowance;
            else
                return 0;
        }

        public override string ToString()
        {
            return "Name of Staff = " + nameOfStaff + ", hourlyRate = " + hourlyRate + ", hWorked = " + hWorked;
        }

        public static void SayHello()
        {
            Console.WriteLine("Hello");
        }
    }
}