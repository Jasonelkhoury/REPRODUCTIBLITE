import java.util.Random;
import java.util.SplittableRandom;
import java.util.random.RandomGenerator;

public class DistributivityFloat32 {

    private static final int REPETITIONS = 10000;
    private static final long SEED = 152;
    private static final double MIN_VALUE = 0.0;
    private static final double MAX_VALUE = 1.0;

    private static final String TYPE_LABEL = "float32";
    private static final String RANDOM_GENERATOR = "JavaRandom";

    public static void main(String[] args) {

        // Random generator selection
        
        RandomGenerator rng = new Random(SEED);
        

        int equalCount = 0;

        for (int i = 0; i < REPETITIONS; i++) {

            // Numeric type selection
            float x = (float)
                (MIN_VALUE + rng.nextDouble() * (MAX_VALUE - MIN_VALUE));

            float y = (float)
                (MIN_VALUE + rng.nextDouble() * (MAX_VALUE - MIN_VALUE));

            float z = (float)
                (MIN_VALUE + rng.nextDouble() * (MAX_VALUE - MIN_VALUE));

            if (x * (y + z) == x * y + x * z) {
                equalCount++;
            }
        }

        int differentCount = REPETITIONS - equalCount;
        double percentage = 100.0 * equalCount / REPETITIONS;

        System.out.printf(
            "{\"property\":\"%s\",\"type\":\"%s\","
            + "\"random_generator\":\"%s\","
            + "\"repetitions\":%d,\"seed\":%d,"
            + "\"min_value\":%s,\"max_value\":%s,"
            + "\"equal_count\":%d,\"different_count\":%d,"
            + "\"percentage\":%.6f}%n",
            "distributivity",
            TYPE_LABEL,
            RANDOM_GENERATOR,
            REPETITIONS,
            SEED,
            Double.toString(MIN_VALUE),
            Double.toString(MAX_VALUE),
            equalCount,
            differentCount,
            percentage
        );
    }
}