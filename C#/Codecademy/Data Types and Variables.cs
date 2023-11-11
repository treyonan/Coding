// Console --------------------------------------------

using System;

namespace GettingInput
{
  class Program
  {
    static void Main()
    {
      // program outputs stuff
      Console.WriteLine("How old are you?");
      string input = Console.ReadLine();
      Console.WriteLine($"You are {input} years old!");
    }
  }
}

// Data Types ---------------------------------------------

using System;

namespace Form
{
  class Program
  {
    static void Main(string[] args)
    {
      // Create Variables
      string name = "Shadow";
      string breed = "Golden Retriever";
      int age = 5;
      double weight = 65.22;
      bool spayed = true;
      // Print variables to the console
      Console.WriteLine(name);
      Console.WriteLine(breed);
      Console.WriteLine(age);
      Console.WriteLine(weight);
      Console.WriteLine(spayed);

    }
  }
}

