#include <iostream>
#include <string>

int count_ones(int m);

int func(int n, int k) {
  if (n < 1 || k < 1 || n & 1) {
    return -1;
  }
  int m = n - 1;
  int m_ones = count_ones(m);
  for (int i = 0; i <= m_ones - k; ++i) {
    m &= m - 1;  // clear rightmost set bit
  }
  return m | 1;  // resume evenness bit
}

int count_ones(int m) {
  int c = 0;
  while (m) {
    m &= m-1;
    ++c;
  }
  return c;
}

int main(int argc, char *argv[]) {
  int n = std::stoi(argv[1]), k = std::stoi(argv[2]);
  std::cout << func(n, k) << "\n";
  return 0;
}
