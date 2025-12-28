<template>
    <footer>
        <div class="container">
            <div class="row">
                <div class="col-md-2 col-sm-4">
                    <ul>
                        <li>
                            <RouterLink to="/">Home</RouterLink>
                        </li>
                        <li>
                            <RouterLink to="/community">Community</RouterLink>
                        </li>
                        <li>
                            <RouterLink to="/about">About</RouterLink>
                        </li>
                    </ul>
                </div>
                <div class="col-md-2 col-sm-4">
                    <ul>
                        <li>
                            <RouterLink to="/questionnaire">Questionnaire</RouterLink>
                        </li>
                        <li>
                            <RouterLink to="/login">Login</RouterLink>
                        </li>
                        <li>
                            <RouterLink to="/register">Register</RouterLink>
                        </li>
                    </ul>
                </div>
                <div class="col-md-2 col-sm-4">
                    <ul>
                        <li>
                            <RouterLink to="/privacy">Privacy Policy</RouterLink>
                        </li>
                        <li>
                            <RouterLink to="/terms">Terms and Services</RouterLink>
                        </li>
                        <li>
                            <RouterLink to="/report">Report</RouterLink>
                        </li>
                    </ul>
                </div>

                <div class="col-md-6 col-sm-12">
                    <h2>About our Wellness App</h2>
                    <p>
                        To enjoy good health, to bring true happiness to one's family, to bring peace to all, one must
                        first
                        discipline and control one's own mind. If a man can control his mind he can find the way to
                        Enlightenment.
                    </p>
                </div>
            </div>

            <div class="row copy-footer">
                <div class="col-sm-6 col-md-3">
                    &copy; {{ new Date().getFullYear() }} Grafreez.com
                </div>
                <div class="col-sm-6 col-md-3 ms-auto text-end">
                    Created with <i class="fa fa-heart"></i>
                </div>
            </div>
        </div>
    </footer>
</template>