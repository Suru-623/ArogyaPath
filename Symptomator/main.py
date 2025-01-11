import ast
from flask import Flask, request, render_template

from services.handler import get_predicted_value, helper

# flask app
app = Flask(__name__, template_folder="templates")

@app.route("/")
def index():
    return render_template('index.html', suggestion="Disease")


# Define a route for the home page
@app.route('/predict', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        message = "Please either write symptoms or you have written misspelled symptoms"

        symptoms = request.form.get('symptoms')
        suggestion = request.form.get('suggestion')

        if suggestion is None or symptoms.strip() == "":
            return render_template('index.html', suggestion="Disease", message='Please fill all the fields')

        if symptoms == "Symptoms":
            return render_template('index.html', suggestion="Disease", message=message)
        else:
            # Split the user's input into a list of symptoms (assuming they are comma-separated)
            user_symptoms = [s.strip() for s in symptoms.split(',')]
            # Remove any extra characters, if any
            user_symptoms = [symptom.strip("[]' ") for symptom in user_symptoms]
            predicted_disease, valid_symptoms = get_predicted_value(user_symptoms)
            if predicted_disease is None:
                return render_template('index.html', suggestion="Disease", message='Please enter valid symptoms')
            else:
                dis_des, precautionsIn, medicationsIn, rec_diet, workoutIn = helper(predicted_disease)

                symptoms = ", ".join(valid_symptoms)

                my_precautions = []

                for i in precautionsIn[0]:
                    my_precautions.append(i)

                if suggestion == "Disease":
                    condition = "red"
                    return render_template('index.html', symptoms=symptoms, suggestion=suggestion, condition=condition,
                                           result=predicted_disease)
                elif suggestion == "Description":
                    condition = "yellow"
                    return render_template('index.html', symptoms=symptoms, suggestion=suggestion, condition=condition,
                                           result=dis_des)
                elif suggestion == "Precaution":
                    condition = "yellow"
                    return render_template('index.html', symptoms=symptoms, suggestion=suggestion, condition=condition,
                                           result=my_precautions)
                elif suggestion == "Medications":
                    condition = "green"
                    medicine_string = medicationsIn[0]
                    medicine_list = ast.literal_eval(medicine_string)
                    medicines = []
                    for i in medicine_list:
                        medicines.append(i)
                    return render_template('index.html', symptoms=symptoms, suggestion=suggestion, condition=condition,
                                           result=medicines)
                elif suggestion == "Diets":
                    condition = "green"
                    diet_string = rec_diet[0]
                    diet_list = ast.literal_eval(diet_string)
                    diet = []
                    for i in diet_list:
                        diet.append(i)
                    return render_template('index.html', symptoms=symptoms, suggestion=suggestion, condition=condition,
                                           result=diet)
                elif suggestion == "Workouts":
                    condition = "green"
                    work = []
                    for i in workoutIn:
                        work.append(i)
                    return render_template('index.html', symptoms=symptoms, suggestion=suggestion, condition=condition,
                                           result=work)

    return render_template('index.html', suggestion="Disease")


# about view funtion and path
@app.route('/about')
def about():
    return render_template("about.html")


# contact view funtion and path
@app.route('/contact')
def contact():
    return render_template("contact.html")


# developer view funtion and path
@app.route('/developer')
def developer():
    return render_template("developer.html")


# about view funtion and path
@app.route('/blog')
def blog():
    return render_template("blog.html")


if __name__ == '__main__':
    app.run(debug=True)
