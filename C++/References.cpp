#include <iostream>

void swap_num(int &i, int &j) {
 
  int temp = i;
  i = j;
  j = temp;
 
}

int main() {
  
  int soda = 99;
  int &pop = soda;
  pop++;
  std::cout << soda << "\n";
  std::cout << pop << "\n";

  int a = 100;
  int b = 200;
 
  swap_num(a, b);
 
  std::cout << "A is " << a << "\n";
  std::cout << "B is " << b << "\n";
    

  int power = 9000;
  
  // Print power memory address
  std::cout << &power << "\n";

}