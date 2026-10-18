import java.io.IOException;
import java.io.PrintWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Locale;
import java.util.Random;

/**
 * Experimentally tests the associativity of IEEE 754 double-precision addition.
 *
 * For random triples (x, y, z), compares (x + y) + z with x + (y + z)
 * using exact equality, counts equal and different outcomes, and writes
 * a summary report to answer_associativity_llm.txt.
 */
public class AssociativityTest {

    // Reproducibility parameters
    private static final long SEED = 42L;
    private static final long NUM_TESTS = 1_000_000L;

    // Interval from which x, y, z are drawn (uniformly)
    private static final double LOW = -1.0e6;
    private static final double HIGH = 1.0e6;

    // Number of counterexamples to record in the output file
    private static final int MAX_EXAMPLES = 10;

    private static final Path OUTPUT_FILE = Path.of("answer_associativity_llm.txt");

    public static void main(String[] args) throws IOException {
        Random rnd = new Random(SEED);

        long equalCount = 0;
        long differentCount = 0;
        StringBuilder examples = new StringBuilder();

        for (long i = 0; i < NUM_TESTS; i++) {
            double x = nextInRange(rnd, LOW, HIGH);
            double y = nextInRange(rnd, LOW, HIGH);
            double z = nextInRange(rnd, LOW, HIGH);

            double leftGrouping = (x + y) + z;   // (x + y) + z
            double rightGrouping = x + (y + z);  // x + (y + z)

            if (leftGrouping == rightGrouping) {  // exact equality
                equalCount++;
            } else {
                differentCount++;
                if (differentCount <= MAX_EXAMPLES) {
                    examples.append(String.format(Locale.ROOT,
                            "  x = %.17g, y = %.17g, z = %.17g%n" +
                            "    (x + y) + z = %.17g%n" +
                            "    x + (y + z) = %.17g%n%n",
                            x, y, z, leftGrouping, rightGrouping));
                }
            }
        }

        double equalPercentage = 100.0 * equalCount / NUM_TESTS;
        String report = buildReport(equalCount, differentCount, equalPercentage, examples);

        System.out.print(report);
        Files.writeString(OUTPUT_FILE, report, StandardCharsets.UTF_8);
        System.out.println("Results written to " + OUTPUT_FILE.toAbsolutePath());
    }

    /** Draws a uniformly distributed double in [low, high). */
    private static double nextInRange(Random rnd, double low, double high) {
        return low + (high - low) * rnd.nextDouble();
    }

    /** Builds the textual report written to the file and printed to stdout. */
    private static String buildReport(long equalCount, long differentCount,
                                      double equalPercentage, StringBuilder examples) {
        StringBuilder sb = new StringBuilder();
        sb.append("Floating-point associativity experiment (double precision)\n");
        sb.append("==========================================================\n");
        sb.append(String.format(Locale.ROOT, "Seed:              %d%n", SEED));
        sb.append(String.format(Locale.ROOT, "Interval:          [%.1f, %.1f)%n", LOW, HIGH));
        sb.append(String.format(Locale.ROOT, "Total tests:       %d%n", NUM_TESTS));
        sb.append(String.format(Locale.ROOT, "Equal results:     %d%n", equalCount));
        sb.append(String.format(Locale.ROOT, "Different results: %d%n", differentCount));
        sb.append(String.format(Locale.ROOT, "Equality rate:     %.4f%%%n", equalPercentage));

        if (differentCount > 0) {
            sb.append(String.format(Locale.ROOT, "%nFirst %d counterexamples:%n", MAX_EXAMPLES));
            sb.append(examples);
        }
        return sb.toString();
    }
}