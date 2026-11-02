import java.io.IOException;
import java.math.BigDecimal;
import java.math.MathContext;
import java.math.RoundingMode;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;

/**
 * Reproducibility lab: the "e-banker" investment.
 *
 * Scheme:
 *   - The client deposits e (Euler's number).
 *   - In year k (k = 1..n): the banker takes a 1 euro fee, then multiplies the balance by k.
 *   - After n years, retrieving the money costs a further 1 euro fee.
 *
 * Recurrence:  B_0 = e,  B_k = (B_{k-1} - 1) * k
 * Closed form: B_n = n! * (e - sum_{j=0}^{n-1} 1/j!) = sum_{m>=0} 1/((n+1)(n+2)...(n+m))
 *
 * Because the simulation subtracts nearly equal quantities and multiplies by n!,
 * double precision is insufficient. This program uses BigDecimal with a 150-digit
 * value of e and 250-digit working precision, then cross-checks the result against
 * the closed-form series.
 *
 * Requires: Java 11+ (tested conceptually against OpenJDK 21.0.11).
 * Output:   prints results to stdout and writes answer_banking_llm.txt in the current directory.
 */
public class BankingLLM {

    private static final int YEARS = 50;
    private static final int E_DIGITS = 150;
    private static final int WORK_PRECISION = 250;
    private static final int DISPLAY_SCALE = 12;
    private static final String OUTPUT_FILE = "answer_banking_llm.txt";

    private static final MathContext MC = new MathContext(WORK_PRECISION, RoundingMode.HALF_EVEN);
    private static final BigDecimal FEE = BigDecimal.ONE;

    public static void main(String[] args) {
        BigDecimal initialBalance = computeE(E_DIGITS);

        BigDecimal balanceBeforeRetrieval = simulate(initialBalance, YEARS);
        BigDecimal finalPayout = balanceBeforeRetrieval.subtract(FEE, MC);

        BigDecimal closedForm = closedFormBalance(YEARS);
        BigDecimal difference = balanceBeforeRetrieval.subtract(closedForm, MC).abs();

        String report = buildReport(initialBalance, balanceBeforeRetrieval, finalPayout, closedForm, difference);

        System.out.print(report);
        writeReport(report);
    }

    /**
     * Computes e = sum_{k>=0} 1/k! to the requested number of significant digits.
     */
    static BigDecimal computeE(int digits) {
        MathContext mc = new MathContext(digits + 30, RoundingMode.HALF_EVEN);
        BigDecimal epsilon = BigDecimal.ONE.movePointLeft(digits + 20);
        BigDecimal sum = BigDecimal.ZERO;
        BigDecimal term = BigDecimal.ONE; // 1/0!

        for (int k = 0; ; k++) {
            if (k > 0) {
                term = term.divide(BigDecimal.valueOf(k), mc); // 1/k! = (1/(k-1)!) / k
            }
            sum = sum.add(term, mc);
            if (term.compareTo(epsilon) < 0) {
                break;
            }
        }
        return sum.round(new MathContext(digits, RoundingMode.HALF_EVEN));
    }

    /**
     * Simulates the scheme year by year: fee of 1 euro, then multiply by the year number.
     */
    static BigDecimal simulate(BigDecimal initial, int years) {
        BigDecimal balance = initial;
        for (int year = 1; year <= years; year++) {
            balance = balance.subtract(FEE, MC)
                             .multiply(BigDecimal.valueOf(year), MC);
        }
        return balance;
    }

    /**
     * Independent closed-form value: B_n = sum_{m>=0} 1/((n+1)(n+2)...(n+m)).
     * Does not use e, so it serves as a cross-check on the simulation.
     */
    static BigDecimal closedFormBalance(int n) {
        BigDecimal epsilon = BigDecimal.ONE.movePointLeft(E_DIGITS + 10);
        BigDecimal sum = BigDecimal.ONE; // m = 0 term
        BigDecimal term = BigDecimal.ONE;

        for (int m = 1; ; m++) {
            term = term.divide(BigDecimal.valueOf((long) n + m), MC);
            sum = sum.add(term, MC);
            if (term.compareTo(epsilon) < 0) {
                break;
            }
        }
        return sum;
    }

    static String buildReport(BigDecimal initial,
                              BigDecimal beforeRetrieval,
                              BigDecimal finalPayout,
                              BigDecimal closedForm,
                              BigDecimal difference) {
        StringBuilder sb = new StringBuilder();
        sb.append("=== Banking investment reproducibility lab ===\n");
        sb.append("Scheme: deposit e; each year take 1 euro fee, multiply by year number; 1 euro retrieval fee at the end.\n\n");

        sb.append("Initial balance (e): ")
          .append(initial.setScale(50, RoundingMode.HALF_EVEN).toPlainString())
          .append(" euros\n");
        sb.append("Number of years: ").append(YEARS).append("\n");
        sb.append("Balance after year ").append(YEARS).append(" (before retrieval fee): ")
          .append(beforeRetrieval.setScale(DISPLAY_SCALE, RoundingMode.HALF_EVEN).toPlainString())
          .append(" euros\n");
        sb.append("Final balance (after 1 euro retrieval fee): ")
          .append(finalPayout.setScale(DISPLAY_SCALE, RoundingMode.HALF_EVEN).toPlainString())
          .append(" euros\n\n");

        sb.append("Cross-check (closed form, independent of e):\n");
        sb.append("  Balance before retrieval fee: ")
          .append(closedForm.setScale(DISPLAY_SCALE, RoundingMode.HALF_EVEN).toPlainString())
          .append(" euros\n");
        sb.append(String.format("  Absolute difference from simulation: %.3e%n", difference.doubleValue()));

        return sb.toString();
    }

    static void writeReport(String report) {
        try {
            Files.writeString(Path.of(OUTPUT_FILE), report, StandardCharsets.UTF_8);
            System.out.println("Results written to " + OUTPUT_FILE);
        } catch (IOException e) {
            System.err.println("Failed to write " + OUTPUT_FILE + ": " + e.getMessage());
            System.exit(1);
        }
    }
}