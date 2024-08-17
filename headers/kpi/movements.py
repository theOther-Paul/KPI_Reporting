import pandas as pd


class EmployeeMovements:
    def __init__(
        self,
        last_q_df,
        actual_q_df,
        department_col="department",
        employee_id_col="employee_id",
    ):
        self.last_q_df = last_q_df
        self.actual_q_df = actual_q_df
        self.department_col = department_col
        self.employee_id_col = employee_id_col

        # Create sets of employee IDs for faster lookup
        self.last_q_ids = set(self.last_q_df[self.employee_id_col])
        self.actual_q_ids = set(self.actual_q_df[self.employee_id_col])

    def get_terminations(self):
        # Employees in last quarter but not in actual quarter
        terminated_ids = self.last_q_ids - self.actual_q_ids
        return self.last_q_df[self.last_q_df[self.employee_id_col].isin(terminated_ids)]

    def get_hires(self):
        # Employees in actual quarter but not in last quarter
        hired_ids = self.actual_q_ids - self.last_q_ids
        return self.actual_q_df[self.actual_q_df[self.employee_id_col].isin(hired_ids)]

    def get_lateral_movements_in(self, department):
        # Employees in the actual department this quarter but were in a different department last quarter
        lateral_in_df = self.actual_q_df[
            self.actual_q_df[self.department_col] == department
        ]
        lateral_in_df = lateral_in_df[
            lateral_in_df[self.employee_id_col].isin(self.last_q_ids)
        ]

        lateral_in_ids = set(lateral_in_df[self.employee_id_col])
        return self.last_q_df[
            (self.last_q_df[self.employee_id_col].isin(lateral_in_ids))
            & (self.last_q_df[self.department_col] != department)
        ]

    def get_lateral_movements_out(self, department):
        # Employees in the actual department last quarter but are now in a different department
        lateral_out_df = self.last_q_df[
            self.last_q_df[self.department_col] == department
        ]
        lateral_out_df = lateral_out_df[
            lateral_out_df[self.employee_id_col].isin(self.actual_q_ids)
        ]

        lateral_out_ids = set(lateral_out_df[self.employee_id_col])
        return self.actual_q_df[
            (self.actual_q_df[self.employee_id_col].isin(lateral_out_ids))
            & (self.actual_q_df[self.department_col] != department)
        ]

    def get_all_movements(self, department):
        terminations = self.get_terminations()
        hires = self.get_hires()
        lateral_in = self.get_lateral_movements_in(department)
        lateral_out = self.get_lateral_movements_out(department)

        return {
            "terminations": terminations,
            "hires": hires,
            "lateral_in": lateral_in,
            "lateral_out": lateral_out,
        }
