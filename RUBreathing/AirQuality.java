/**
 *  This file is the data portion for AirNode? we'll see
 * 
 * 
 * 
 * @author Srimathi Vadivel
 * @author Anna Lu
 */

import java.time.LocalDateTime;
import java.util.List;

public class AirQuality {
    private int AQI; // AQI value
    private List<String> primaryPollutants; // list of primary pollutants
    private String healthRecommendations; // health recommendations based on AQI
    private String weatherConditions; // weather conditions at the time of data collection
    private String AQIColor; // color scale based on the AQI value

    public AirQuality(int AQI, List<String> primaryPollutants, String healthRecommendations, 
                      LocalDateTime timestamp, String weatherConditions, String dataSource, String AQIColor) {
        this.AQI = AQI;
        this.primaryPollutants = primaryPollutants;
        this.healthRecommendations = healthRecommendations;
        this.weatherConditions = weatherConditions;
        this.AQIColor = AQIColor;
    }

    // getters and setters
    public int getAQI() { return AQI; }
    public void setAQI(int AQI) { this.AQI = AQI; }

    public List<String> getPrimaryPollutants() { return primaryPollutants; }
    public void setPrimaryPollutants(List<String> primaryPollutants) { this.primaryPollutants = primaryPollutants; }

    public String getHealthRecommendations() { return healthRecommendations; }
    public void setHealthRecommendations(String healthRecommendations) { this.healthRecommendations = healthRecommendations; }

    public String getWeatherConditions() { return weatherConditions; }
    public void setWeatherConditions(String weatherConditions) { this.weatherConditions = weatherConditions; }

    public String getAQIColor() { return AQIColor; }
    public void setWeatherConditions(String AQIColor) { this.AQIColor = AQIColor; }

}
