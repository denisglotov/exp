#include <iostream>

int main() {
  int currencies_num = 0;
  std::cin >> currencies_num;
  if (currencies_num < 1) {
    std::cerr << "Invalid currencies number.\n";
    return -1;
  }

  double rate[currencies_num][currencies_num],
    profit[currencies_num][currencies_num],
    profit_next[currencies_num][currencies_num];
  std::string path[currencies_num][currencies_num];

  for (int i = 0; i != currencies_num; ++i) {
    for (int j = 0; j != currencies_num; ++j) {
      std::cin >> rate[i][j];
      profit[i][j] = rate[i][j];
      path[i][j] = std::string(1, '0' + i) + std::string(1, '0' + j);
    }
  }

  for (int step = 0; step != currencies_num; ++step) {
    for (int i = 0; i != currencies_num; ++i) {
      for (int j = 0; j != currencies_num; ++j) {
        if (i == j && j == step) {
          continue;
        }
        const double alt_profit = profit[i][step] * profit[step][j];
        if (profit[i][j] >= alt_profit) {
          profit_next[i][j] = profit[i][j];
        } else {
          profit_next[i][j] = alt_profit;
          path[i][j] = "(" + path[i][step] + ":" +  path[step][j] + ")";
        }
      }
    }

    // Update `profit` matrix with next step values.
    for (int i = 0; i != currencies_num; ++i) {
      for (int j = 0; j != currencies_num; ++j) {
        profit[i][j] = profit_next[i][j];
      }
    }
  }

  for (int i = 0; i != currencies_num; ++i) {
    std::cout << profit[i][i] << ":\t" << path[i][i] << '\n';
  }

  return 0;
}
