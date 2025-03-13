namespace CSProject;

class Manager : Staff
{
    private const float managerHourlyRate = 50;

    public int Allowance { get; private set; }

    public Manager(string name) : base(name, managerHourlyRate)
    {
    }

    public override void CalculatePay()
    {
        base.CalculatePay();
        Allowance = 1000;

        if (HoursWorked > 160)
        {
            TotalPay += Allowance;
        }
    }

    public override string ToString()
    {
        return $"Name: {NameOfStaff}\nHourly Rate: {managerHourlyRate}\nHours Worked: {HoursWorked}\nBasic Pay: {BasicPay}\nAllowance: {Allowance}\nTotal Pay: {TotalPay}";
    }
}