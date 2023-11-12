// Hello World --------------------------------------------

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

// Creating Variables with Types ----------------------------------

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

// Converting Data Types

using System;

namespace FavoriteNumber
{
  class Program
  {
    static void Main(string[] args)
    {
      // Ask user for fave number
      Console.Write("Enter your favorite number!: ");

      // Turn that answer into an int
      
      // Attempt 1: use implicit conversion
      // int faveNumber = Console.ReadLine();
      
      // Attempt 2: use explicit conversion
      // int faveNumber = (int)Console.ReadLine();
      
      // Attempt 3: use Convert method
      int faveNumber = Convert.ToInt32(Console.ReadLine());

    }
  }
}


