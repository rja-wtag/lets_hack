import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col">
      <section className="flex-1 flex flex-col items-center justify-center text-center py-20 px-6">
        <h2 className="text-5xl font-bold mb-6">We Build Software That Works</h2>
        <p className="text-lg text-muted-foreground max-w-2xl mb-8">
          Empowering businesses with cutting-edge technology solutions, tailored to your needs. From
          web apps to mobile — we’ve got you covered.
        </p>
        <div className="flex gap-4">
          <Button asChild>
            <Link to="/contact">Get Started</Link>
          </Button>
          <Button variant="outline" asChild>
            <Link to="/services">Learn More</Link>
          </Button>
        </div>
      </section>

      {/* Features */}
      <section className="py-16 bg-muted/30">
        <div className="container mx-auto px-6">
          <h3 className="text-3xl font-bold text-center mb-12">Our Services</h3>
          <div className="grid gap-8 md:grid-cols-3">
            <Card>
              <CardHeader>
                <CardTitle>Custom Web Apps</CardTitle>
              </CardHeader>
              <CardContent>
                Build scalable, secure, and performant web applications designed for your business
                needs.
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Mobile Development</CardTitle>
              </CardHeader>
              <CardContent>
                Create intuitive mobile apps with seamless experiences for iOS and Android.
              </CardContent>
            </Card>
            <Card>
              <CardHeader>
                <CardTitle>Cloud Solutions</CardTitle>
              </CardHeader>
              <CardContent>
                Harness the power of the cloud with robust, cost-effective, and scalable
                infrastructure.
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-6 mt-auto">
        <div className="container mx-auto px-6 text-center text-sm text-muted-foreground">
          © {new Date().getFullYear()} SoftCo. All rights reserved.
        </div>
      </footer>
    </div>
  );
}
