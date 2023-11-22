import streamlit as st
from utils import add_logo,add_contact_info,configure_streamlit_page,open_ai_key
import pandas as pd
import streamlit as st 
from function import visualize_timeseries ,yoy_growth,calculate_trend_slope_dataframe,\
model,find_max_min_volume_months
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate


##Page Configuration
configure_streamlit_page()
add_logo()
openai_api_key=open_ai_key()
add_contact_info()

##Reading the data
df_dash = pd.read_csv("Data/Diageo_gen.csv")

#st.markdown("#### <span style='color: #265B8C;'>Explore Granular Details</span>", unsafe_allow_html=True)
st.markdown("#### <p style='color: dark grey;'><b>Are you looking to dive deep into specific details? I'm here to help!</b></p>", unsafe_allow_html=True)
st.markdown("###### <span style='color: #265B8C;'>Select Your Parameter</span>", unsafe_allow_html=True)

def main():
    """
    Tab for visualizing and analyzing time series data using an AI model.

    """
        

    def select_level(d):
        """
            Select data levels and additional options.

            Parameters:
            - d: DataFrame containing the data.

            Returns:
            - A tuple containing selected levels and other options.
            """
            
            

        # Create a list to store selected options
        selected_levels = []
        col_cou1,col_cou2,col_cou3,col_cou4=st.columns(4)
        with col_cou1:
            geo_options = d["geo"].unique().tolist()
            selected_geo = st.selectbox("Country", geo_options)
            d = d[d["geo"] == selected_geo]
            selected_levels.append("geo")
        c1,c2,c3,c4=st.columns(4)

        with c1:
            st.markdown("###### <span style='color: #265B8C;'>Select Hierarchy</span>", unsafe_allow_html=True)
            # Create columns for checkboxes
        col1, col2, col3 = st.columns(3)
            
            #Create a checkbox for each level
        with col1:
            checkbox = st.checkbox("###### :red[Channel] 🛒", value="channel" in selected_levels, key="channel")
            if checkbox:
                    selected_levels.append("channel")

        with col2:
            checkbox = st.checkbox("###### :red[Sector] 🍺", value="sector" in selected_levels, key="sector")
            if checkbox:
                selected_levels.append("sector")

        with col3:
            checkbox = st.checkbox("###### :red[Price Tier] 💲", value="price_tier" in selected_levels, key="price_tier")
            if checkbox:
                selected_levels.append("price_tier")
        #selected_geo="Great Britain"
        selected_channel = None
        selected_sector = None
        selected_price_tier = None
        # Create columns for select boxes
        col1, col2, col3= st.columns(3)
        with col1:
            if "channel" in selected_levels:
                channel_options = d["channel"].unique().tolist()
                    #st.markdown('<p style="border: 2px solid red; padding: 1px; font-weight: bold;color: #265B8C;size:4;">Select Channel:</p>', unsafe_allow_html=True)
                selected_channel = st.selectbox("Select Channel", channel_options)
                d=d[d["channel"]==selected_channel]

        with col2:
            if "sector" in selected_levels:
                sector_options = d["sector"].unique().tolist()
                    #st.markdown('<p style="border: 2px solid red; padding: 1px; font-weight: bold;color: #265B8C;size:4;">Select Sector:</p>', unsafe_allow_html=True)
                selected_sector = st.selectbox("Select Sector", sector_options)
                d=d[d["sector"]==selected_sector]

        with col3:
            if "price_tier" in selected_levels:
                price_tier_options = d["price_tier"].unique().tolist()
                    #st.markdown('<p style="border: 2px solid red; padding: 1px; font-weight: bold;color: #265B8C;size:4;">Select Price Tier:</p>', unsafe_allow_html=True)
                selected_price_tier = st.selectbox("Select Price Tier", price_tier_options)

        return selected_levels, selected_channel, selected_sector, selected_price_tier,selected_geo




# Select data levels and additional options
    selected_levels = select_level(df_dash)
    # Time Series Visualization Section
    st.markdown("---")
    data = visualize_timeseries(df_dash, selected_levels[0], selected_levels[4],
                                    selected_levels[1], selected_levels[2], selected_levels[3])
        

        
    data_trend = calculate_trend_slope_dataframe(data)
    seasonal_patter_dict=find_max_min_volume_months(data)
    if data_trend is None:
        pass
    elif data_trend.empty:
        pass
    else:
        data_trend_2 = data_trend.groupby(["scenario", "trend"])[["slope_his", "slope_for"]].mean().reset_index()
        trend_dict=data_trend_2[["scenario","trend"]].set_index("scenario")["trend"].to_dict()
    if data.empty:
        pass
    else:
        data_yoy_dict = yoy_growth(data)  
        
        # Generate AI-driven analysis
    m = st.markdown("""
    <style>
    div.stButton {
        display: flex;
        justify-content: flex-end;
    }
    div.stButton > button:first-child {
        background-color: #FF4B4B;
        color:#ffffff;
    }
    div.stButton > button:hover {
        background-color: blue;
        color:#ff0000;
        }
    </style>""", unsafe_allow_html=True)
    if st.button("Get Analysis"):
        analysis_string = """Generate the analysis based on instruction\
                                that is delimited by triple backticks.\
                                instruction: ```{instruction_analyis}```
                                in the format enclosed in html tag <{format_analysis}\>\
                                """
        analysis_template = ChatPromptTemplate.from_template(analysis_string)

        format_analysis=f"""
            1.Historical Trends:
                Review of past trends

            2.Forecasted Trends:
                Predicted future trends

            3.Seasonality Analysis:
                Examining in genral seasonal patterns in the data(max,min sales months )
            
            4.Year-on-Year (YoY) Growth Analysis:
                Summarizes year-over-year growth 

            5.Conclusion: 
                Conclusion based on the time series analysis"""

        instruction_analysis = f"""You are functioning as an AI data analyst.
            1. You will be analyzing three dictinoary: trend_dict,data_yoy_dict and seasonal_patter_dict.
            2. Trend_dict key represent scenario: Indicates if a data point is historical or forecasted and value\
                Trend: Indicates the trend of the data for a specific scenario.
            3. data_yoy_dict key represet year and value Indicates the percentage volume change compared to the previous year  
            4. Start the output as "Insight and Findings:" and report in point form.
            5. Summarizes the trend based on the Trend_dict
            6. Analyze the year on year growth based on the data_yoy_dict include the change percentage.
            7. Analyze the in general seasonality based on the seasonal_patter_dict
            8. The dictinoary: {trend_dict} for trend analysis,{data_yoy_dict} for year-on-year growth analysis and  {seasonal_patter_dict} for seasonlity analysis.
            9. Donot include the name of dict only generate inshits from using the dict data"""

        chat = ChatOpenAI(temperature=0.0, model=model, openai_api_key=openai_api_key)
        user_analysis = analysis_template.format_messages(instruction_analyis=instruction_analysis,format_analysis=format_analysis)

        with st.spinner('Generating...'):
            st.markdown("###### <span style='color: #265B8C;'>Inshights and Findings</span>", unsafe_allow_html=True)

            response = chat(user_analysis)
            text=response.content
            # Define the headings of interest
            headings_of_interest = ["Historical Trends", "Forecasted Trends", "Seasonality Analysis", "Year-on-Year (YoY) Growth Analysis", "Conclusion"]

            # Initialize a dictionary to store the sections
            result_dict = {heading: "" for heading in headings_of_interest}

            # Split the text based on each heading
            for heading in headings_of_interest:
                start_idx = text.find(heading)
                end_idx = text.find(headings_of_interest[(headings_of_interest.index(heading) + 1) % len(headings_of_interest)]) if headings_of_interest.index(heading) + 1 < len(headings_of_interest) else None
                result_dict[heading] = text[start_idx:end_idx].strip().replace(heading, "").strip()[1:]
                            
                # Apply styling to the output box with a chat icon
            
            c1,c2,c3,c4,c5=st.columns(5)
       
            with c1:
                heading_of_interest = headings_of_interest[0]

                # Use HTML tags to style the heading and content
                styled_text = (
                    f'<div style="border: 1px solid #265B8C; padding: 3px; background-color: orange; color: black;border-radius: 5px;width: 220px; height: 350px;"">'
                    f'<div style="font-size: 18px; color: black;"><b>{heading_of_interest}:</b></div>' 
                    f"{result_dict[heading_of_interest]}"
                    f'</div>'
                )

                # Display the styled text using Streamlit's markdown
                st.markdown(styled_text, unsafe_allow_html=True)
            with c2:
                heading_of_interest = headings_of_interest[1]

                # Use HTML tags to style the heading and content
                styled_text = (
                    f'<div style="border: 1px solid #265B8C; padding: 3px; background-color: orange; color: black;border-radius: 5px;width: 220px; height: 350px;"">'
                    f'<div style="font-size: 18px; color:black;"><b>{heading_of_interest}:</b></div>' 
                    f"{result_dict[heading_of_interest]}"
                    f'</div>'
                )

                # Display the styled text using Streamlit's markdown
                st.markdown(styled_text, unsafe_allow_html=True)                  
            with c3:
                heading_of_interest = headings_of_interest[2]

                # Use HTML tags to style the heading and content
                styled_text = (
                    f'<div style="border: 1px solid #265B8C; padding: 3px; background-color: orange; color: black;border-radius: 5px;width: 220px; height: 350px;"">'
                    f'<div style="font-size: 18px; color: black;"><b>{heading_of_interest}:</b></div>' 
                    f"{result_dict[heading_of_interest]}"
                    f'</div>'
                )

                # Display the styled text using Streamlit's markdown
                st.markdown(styled_text, unsafe_allow_html=True)
            with c4:
                heading_of_interest = headings_of_interest[3]

                # Use HTML tags to style the heading and content
                styled_text = (
                    f'<div style="border: 1px solid #265B8C; padding: 3px; background-color: orange; color: black;border-radius: 5px;width: 220px; height: 350px;"">'
                    f'<div style="font-size: 18px; color: black;"><b>{heading_of_interest}:</b></div>' 
                    f"{result_dict[heading_of_interest]}"
                    f'</div>'
                )

                # Display the styled text using Streamlit's markdown
                st.markdown(styled_text, unsafe_allow_html=True)
            with c5:
                heading_of_interest = headings_of_interest[4]

                # Use HTML tags to style the heading and content
                styled_text = (
                    f'<div style="border: 1px solid #265B8C; padding: 3px; background-color: green; color: white;border-radius: 5px;width: 220px; height: 350px;"">'
                    f'<div style="font-size: 18px; color: white;"><b>{heading_of_interest}:</b></div>' 
                    f"{result_dict[heading_of_interest]}"
                    f'</div>'
                )

                # Display the styled text using Streamlit's markdown
                st.markdown(styled_text, unsafe_allow_html=True)

                    

    st.markdown("---")

if __name__ == "__main__":
    main()


