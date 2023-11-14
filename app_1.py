from flask import Flask, render_template, request
import pandas as pd
import numpy as np

# Load the CSV file using pandas
popular_df = pd.read_csv('popular.csv')
pt = pd.read_csv('pt.csv')
books = pd.read_csv('books.csv')
similarity_scores = pd.read_csv('similarity_score.csv')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html",
                           book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['Num-Ratings'].values),
                           rating=list(popular_df['avg_rating'].values)
                           )

@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    data = []  # Initialize the data variable

    # Check if user_input is in pt['Book-Title'].values
    if user_input in pt['Book-Title'].values:
        index = np.where(pt['Book-Title'] == user_input)[0][0]

        # Check if index is within the valid range of similarity_scores
        if 0 <= index < len(similarity_scores):
            # Get the indices of the top similar items
            similar_items_indices = sorted(range(len(similarity_scores.iloc[index])), key=lambda x: similarity_scores.iloc[index, x], reverse=True)[1:5]

            for i in similar_items_indices:
                item = []
                # Use iloc to access DataFrame rows by integer index
                temp_df = books[books['Book-Title'] == pt.iloc[i]['Book-Title']]

                # Check if temp_df is not empty before accessing its values
                if not temp_df.empty:
                    item.extend(temp_df.drop_duplicates('Book-Title')['Book-Title'].values)
                    item.extend(temp_df.drop_duplicates('Book-Title')['Book-Author'].values)
                    item.extend(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values)

                    data.append(item)
                else:
                    # Handle the case where temp_df is empty
                    pass

            print(data)
        else:
            # Handle the case where index is out of bounds
            print("Index is out of bounds.")
    else:
        # Handle the case where user_input is not found in pt['Book-Title'].values
        print("User input not found in pt['Book-Title'].values.")


    return render_template('recommend.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)
