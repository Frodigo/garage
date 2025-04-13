namespace CSProject
{
    static class FileReader
    {
        static public List<Staff> ReadFile()
        {
            List<Staff> myStaff = new List<Staff>();
            string[] result = new string[2];
            string path = "staff.txt";
            string[] separator = { ", " };

            if (File.Exists(path))
            {
                using (StreamReader sr = new StreamReader(path))
                {
                    while (!sr.EndOfStream)
                    {
                        string line = sr.ReadLine()!;
                        if (line != null)
                        {
                            result = line.Split(separator, StringSplitOptions.RemoveEmptyEntries);
                            if (result[1] == "Manager")
                            {
                                myStaff.Add(new Manager(result[0]));
                            }
                            else if (result[1] == "Admin")
                            {
                                myStaff.Add(new Admin(result[0]));
                            }
                        }
                    }
                    sr.Close();
                }
            }
            else
            {
                Console.WriteLine("Error: File does not exist.");
            }

            return myStaff;
        }
    }
}
