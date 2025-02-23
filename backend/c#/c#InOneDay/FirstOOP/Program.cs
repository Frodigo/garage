using FirstOOP;

class Program
{
    static void Main(string[] args)
    {
        int pay;

        Staff.SayHello();

        Staff staff1 = new Staff("Peter");
        staff1.HoursWorked = 160;
        pay = staff1.CalculatePay(1000, 400);
        Console.WriteLine("Pay = {0}", pay);

        Staff staff2 = new Staff("Filip", "Kwiatkowski");
        staff2.HoursWorked = 220;
        pay = staff2.CalculatePay();
        Console.WriteLine("Pay = {0}", pay);

        Console.WriteLine("----------------");

        // NormalMember member1 = new NormalMember("Special Rate", "James", 1, 2010);
        // VIPMember member2 = new VIPMember("Andy", 2, 2011);

        // member1.CalculateAnnualFee();
        // member2.CalculateAnnualFee();

        // Console.WriteLine(member1.ToString());
        // Console.WriteLine(member2.ToString());

        Member[] clubMembers = new Member[5];

        clubMembers[0] = new NormalMember("Special Rate", "James", 1, 2010);
        clubMembers[1] = new NormalMember("Normal Rate", "Andy", 2, 2011);
        clubMembers[2] = new NormalMember("Normal Rate", "Bill", 3, 2011);
        clubMembers[3] = new VIPMember("Carol", 4, 2012);
        clubMembers[4] = new VIPMember("Evelyn", 5, 2012);

        foreach (Member m in clubMembers)
        {
            m.CalculateAnnualFee();
            Console.WriteLine(m.ToString());
        }
    }
}