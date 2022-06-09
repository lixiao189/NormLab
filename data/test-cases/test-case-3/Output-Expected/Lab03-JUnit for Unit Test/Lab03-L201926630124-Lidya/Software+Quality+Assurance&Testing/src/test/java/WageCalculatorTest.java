import org.junit.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class WageCalculatorTest {

    @ParameterizedTest
    @CsvSource({"800, 40, 0, 20", "950, 45, 0, 20", "1280, 48, 8, 20"})
    void calculatewageParameterizedTest(int expected, int standardhours, int holidayhours, int hourlywage) {
        assertEquals(expected, new WageCalculator().wagescalculator(standardhours, holidayhours, hourlywage));
    }
}
