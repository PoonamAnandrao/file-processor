import os
import csv
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet

class FileProcessorViewSet(ViewSet):
    @action(methods=['POST'], detail=False, url_path='file/processor')
    def file_processor(self, request):
        try:
            input_dir = request.data.get('input_file_path', "")
            output_dir = request.data.get('output_file_path', "")

            if not input_dir:
                return Response({'status': False, 'message': 'Input directory path is missing.'}, status=status.HTTP_400_BAD_REQUEST)
            if not output_dir:
                return Response({'status': False, 'message': 'Output directory path is missing.'}, status=status.HTTP_400_BAD_REQUEST)

            processed_data = []
            for filename in os.listdir(input_dir):
                if filename.endswith(".dat"):
                    with open(os.path.join(input_dir, filename), 'r') as file:
                        for line in file:
                            data = line.strip().split('\t')
                            try:  
                                first_name = data[1]
                                last_name = data[2]
                                email = data[3]
                                job_title = data[4]
                                basic_salary = float(data[5])
                                allowances = float(data[6])
                                gross_salary = basic_salary + allowances

                                processed_data.append({
                                    'first_name': first_name,
                                    'last_name': last_name,
                                    'email': email,
                                    'job_title': job_title,
                                    'basic_salary': basic_salary,
                                    'allowances': allowances,
                                    'gross_salary': gross_salary
                                })
                            except (ValueError, IndexError) as e:
                                pass

            # Sort processed_data by gross_salary in descending order
            sorted_data = sorted(processed_data, key=lambda x: x['gross_salary'], reverse=True)

            # Generate output CSV file
            output_file_path = os.path.join(output_dir, 'result.csv')
            with open(output_file_path, 'w', newline='') as output_file:
                writer = csv.writer(output_file)
                writer.writerow(['first_name', 'last_name', 'email', 'job_title', 'basic_salary', 'allowances', 'gross_salary'])
                for data in sorted_data:
                    writer.writerow([
                        data['first_name'],
                        data['last_name'],
                        data['email'],
                        data['job_title'],
                        data['basic_salary'],
                        data['allowances'],
                        data['gross_salary']
                    ])

                # Write footer values
                second_highest_salary = sorted_data[1]['gross_salary'] if len(sorted_data) > 1 else 0
                average_salary = sum(data['gross_salary'] for data in sorted_data) / len(sorted_data) if sorted_data else 0
                writer.writerow(['Second Highest Salary', second_highest_salary])
                writer.writerow(['average_salary', average_salary])

            return Response({"status": True, "message": "File saved successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"status": False, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
